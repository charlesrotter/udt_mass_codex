#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const zlib = require('zlib');

const SOURCES = path.resolve(__dirname, '..', 'sources');
const N_FROZEN = 1.0559332414320268;

function radiusShapeFromScale(scale) {
  return N_FROZEN * (-Math.expm1((-2.0 * Math.log(scale)) / N_FROZEN));
}

function modelFullScreen(z) {
  const scale = 1.0 + z;
  const radius = radiusShapeFromScale(scale);
  return 5.0 * Math.log10(scale * scale * radius);
}

function modelDeletedScreen(z) {
  const scale = 1.0 + z;
  return 5.0 * Math.log10(scale * scale);
}

function modelDuplicatedScreen(z) {
  const scale = 1.0 + z;
  const radius = radiusShapeFromScale(scale);
  return 5.0 * Math.log10(scale * scale * radius * radius);
}

function modelWrongTransfer(z) {
  const scale = 1.0 + z;
  const radius = radiusShapeFromScale(scale);
  return 5.0 * Math.log10(Math.pow(scale, 1.5) * radius);
}

function dot(a, b) {
  let s = 0.0;
  for (let i = 0; i < a.length; i++) s += a[i] * b[i];
  return s;
}

function solveLowerInPlace(L, n, b) {
  const x = new Float64Array(b);
  for (let i = 0; i < n; i++) {
    let sum = x[i];
    const row = i * n;
    for (let j = 0; j < i; j++) sum -= L[row + j] * x[j];
    x[i] = sum / L[row + i];
  }
  return x;
}

function solveUpperFromLowerTransposeInPlace(L, n, b) {
  const x = new Float64Array(b);
  for (let i = n - 1; i >= 0; i--) {
    let sum = x[i];
    for (let j = i + 1; j < n; j++) sum -= L[j * n + i] * x[j];
    x[i] = sum / L[i * n + i];
  }
  return x;
}

function choleskyLowerInPlace(a, n) {
  for (let i = 0; i < n; i++) {
    const rowI = i * n;
    for (let j = 0; j <= i; j++) {
      let sum = a[rowI + j];
      const rowJ = j * n;
      for (let k = 0; k < j; k++) sum -= a[rowI + k] * a[rowJ + k];
      if (i === j) {
        if (!(sum > 0.0)) throw new Error(`non-positive pivot at ${i}`);
        a[rowI + i] = Math.sqrt(sum);
      } else {
        a[rowI + j] = sum / a[rowJ + j];
      }
    }
  }
}

function profileFromCholesky(L, n, observed, model) {
  const ones = new Float64Array(n);
  const residual = new Float64Array(n);
  for (let i = 0; i < n; i++) {
    ones[i] = 1.0;
    residual[i] = observed[i] - model[i];
  }
  const oneWhite = solveLowerInPlace(L, n, ones);
  const residualWhite = solveLowerInPlace(L, n, residual);
  const offset = dot(oneWhite, residualWhite) / dot(oneWhite, oneWhite);
  let chi2 = 0.0;
  for (let i = 0; i < n; i++) {
    const v = residualWhite[i] - offset * oneWhite[i];
    chi2 += v * v;
  }
  return { chi2, offset };
}

function profileFromPrecision(precision, n, observed, model) {
  const residual = new Float64Array(n);
  for (let i = 0; i < n; i++) residual[i] = observed[i] - model[i];
  let unitPu = 0.0;
  let unitPr = 0.0;
  const pr = new Float64Array(n);
  for (let i = 0; i < n; i++) {
    let rowSumUnit = 0.0;
    let rowSumResidual = 0.0;
    const row = i * n;
    for (let j = 0; j < n; j++) {
      const pij = precision[row + j];
      rowSumUnit += pij;
      rowSumResidual += pij * residual[j];
    }
    unitPu += rowSumUnit;
    unitPr += rowSumResidual;
    pr[i] = rowSumResidual;
  }
  const offset = unitPr / unitPu;
  let chi2 = 0.0;
  for (let i = 0; i < n; i++) {
    const centered = residual[i] - offset;
    chi2 += centered * pr[i];
  }
  return { chi2, offset };
}

async function readPantheon() {
  const dataPath = path.join(SOURCES, '11_Pantheon+SH0ES.dat');
  const stream = fs.createReadStream(dataPath, { encoding: 'utf8' });
  const rl = readline.createInterface({ input: stream, crlfDelay: Infinity });
  let headers = null;
  let zAll = [];
  let obsAll = [];
  let keepIndices = [];
  let idx = 0;
  let iZ = -1, iObs = -1, iCal = -1;
  for await (const line of rl) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    if (!headers) {
      headers = trimmed.split(/\s+/);
      iZ = headers.indexOf('zCMB');
      iObs = headers.indexOf('m_b_corr');
      iCal = headers.indexOf('IS_CALIBRATOR');
      continue;
    }
    const parts = trimmed.split(/\s+/);
    const z = Number(parts[iZ]);
    const obs = Number(parts[iObs]);
    const cal = Number(parts[iCal]);
    zAll.push(z);
    obsAll.push(obs);
    if (z > 0.023 && cal === 0) keepIndices.push(idx);
    idx += 1;
  }

  const covPath = path.join(SOURCES, '12_Pantheon+SH0ES_STAT+SYS.cov');
  const cov = await new Promise((resolve, reject) => {
    const rlCov = readline.createInterface({
      input: fs.createReadStream(covPath, { encoding: 'utf8' }),
      crlfDelay: Infinity,
    });
    let dim = null;
    let keepPos = null;
    let covLocal = null;
    let i = 0;
    let j = 0;
    rlCov.on('line', line => {
      const trimmed = line.trim();
      if (!trimmed) return;
      if (dim === null) {
        dim = Number(trimmed);
        keepPos = new Int32Array(dim).fill(-1);
        for (let k = 0; k < keepIndices.length; k++) keepPos[keepIndices[k]] = k;
        covLocal = new Float64Array(keepIndices.length * keepIndices.length);
        return;
      }
      const ii = keepPos[i];
      const jj = keepPos[j];
      if (ii !== -1 && jj !== -1) covLocal[ii * keepIndices.length + jj] = Number(trimmed);
      j += 1;
      if (j === dim) {
        j = 0;
        i += 1;
      }
    });
    rlCov.on('close', () => resolve(covLocal));
    rlCov.on('error', reject);
  });
  // Symmetrize to match the package path.
  for (let i = 0; i < keepIndices.length; i++) {
    const rowI = i * keepIndices.length;
    for (let j = 0; j < i; j++) {
      const a = cov[rowI + j];
      const b = cov[j * keepIndices.length + i];
      const s = 0.5 * (a + b);
      cov[rowI + j] = s;
      cov[j * keepIndices.length + i] = s;
    }
  }
  const z = new Float64Array(keepIndices.length);
  const obs = new Float64Array(keepIndices.length);
  for (let i = 0; i < keepIndices.length; i++) {
    z[i] = zAll[keepIndices[i]];
    obs[i] = obsAll[keepIndices[i]];
  }
  return { z, observed: obs, covariance: cov, nAll: zAll.length, nKeep: keepIndices.length };
}

function parseNpy(buffer) {
  if (buffer.toString('latin1', 0, 6) !== '\x93NUMPY') throw new Error('bad npy magic');
  const major = buffer[6];
  let headerLen, offset;
  if (major === 1) {
    headerLen = buffer.readUInt16LE(8);
    offset = 10;
  } else if (major === 2) {
    headerLen = buffer.readUInt32LE(8);
    offset = 12;
  } else {
    throw new Error(`unsupported npy version ${major}`);
  }
  const header = buffer.toString('latin1', offset, offset + headerLen);
  const descr = /'descr':\s*'([^']+)'/.exec(header)[1];
  const shapeText = /'shape':\s*\(([^)]*)\)/.exec(header)[1].trim();
  const shape = shapeText
    .split(',')
    .map(s => s.trim())
    .filter(Boolean)
    .map(Number);
  const data = buffer.subarray(offset + headerLen);
  return { descr, shape, data };
}

function readNpzEntry(npzPath, entryName) {
  const buf = fs.readFileSync(npzPath);
  let off = 0;
  while (off < buf.length) {
    if (buf.readUInt32LE(off) !== 0x04034b50) throw new Error('bad zip local header');
    const method = buf.readUInt16LE(off + 8);
    const compSize = buf.readUInt32LE(off + 18);
    const nameLen = buf.readUInt16LE(off + 26);
    const extraLen = buf.readUInt16LE(off + 28);
    const name = buf.toString('utf8', off + 30, off + 30 + nameLen);
    const dataStart = off + 30 + nameLen + extraLen;
    const comp = buf.subarray(dataStart, dataStart + compSize);
    if (name === entryName) {
      const raw = method === 0 ? comp : zlib.inflateRawSync(comp);
      return parseNpy(raw);
    }
    off = dataStart + compSize;
  }
  throw new Error(`missing ${entryName}`);
}

async function readDes() {
  const dataPath = path.join(SOURCES, '13_DES-Dovekie_HD.csv');
  const stream = fs.createReadStream(dataPath, { encoding: 'utf8' });
  const rl = readline.createInterface({ input: stream, crlfDelay: Infinity });
  let names = null;
  const rows = [];
  for await (const raw of rl) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    if (line.startsWith('VARNAMES:')) {
      names = line.split(/\s+/).slice(1);
      continue;
    }
    if (!line.startsWith('SN:')) continue;
    const parts = line.split(/\s+/).slice(1);
    const row = {};
    for (let i = 0; i < names.length; i++) row[names[i]] = parts[i];
    rows.push(row);
  }
  const keep = [];
  const z = [];
  const observed = [];
  for (let i = 0; i < rows.length; i++) {
    if (Number(rows[i].IDSURVEY) === 10) {
      keep.push(i);
      z.push(Number(rows[i].zHD));
      observed.push(Number(rows[i].MU));
    }
  }
  const npzPath = path.join(SOURCES, '14_STAT+SYS.npz');
  const nsn = readNpzEntry(npzPath, 'nsn.npy');
  const covPacked = readNpzEntry(npzPath, 'cov.npy');
  const dim = Number(covPacked.shape[0] ? Math.round((Math.sqrt(8 * covPacked.shape[0] + 1) - 1) / 2) : 0);
  const nsnValue = Number(new BigInt64Array(
    nsn.data.buffer,
    nsn.data.byteOffset,
    nsn.data.byteLength / 8
  )[0]);
  if (nsnValue !== dim) throw new Error(`DES dimension mismatch ${nsnValue} vs ${dim}`);
  const packed = new Float32Array(
    covPacked.data.buffer,
    covPacked.data.byteOffset,
    covPacked.data.byteLength / 4
  );
  return {
    keep: Int32Array.from(keep),
    z: Float64Array.from(z),
    observed: Float64Array.from(observed),
    dimension: dim,
    packed,
    nAll: rows.length,
    nKeep: keep.length,
  };
}

function packedUpperGet(packed, n, i, j) {
  if (i > j) {
    const t = i;
    i = j;
    j = t;
  }
  return packed[i * n - (i * (i - 1)) / 2 + (j - i)];
}

function buildDesMarginalPrecision(des) {
  const n = des.dimension;
  const keep = Array.from(des.keep);
  const keepSet = new Set(keep);
  const drop = [];
  for (let i = 0; i < n; i++) if (!keepSet.has(i)) drop.push(i);
  const nk = keep.length;
  const nd = drop.length;
  const A = new Float64Array(nk * nk);
  const B = new Float64Array(nk * nd);
  const D = new Float64Array(nd * nd);

  for (let i = 0; i < nk; i++) {
    const gi = keep[i];
    const rowA = i * nk;
    const rowB = i * nd;
    for (let j = 0; j < nk; j++) A[rowA + j] = packedUpperGet(des.packed, n, gi, keep[j]);
    for (let j = 0; j < nd; j++) B[rowB + j] = packedUpperGet(des.packed, n, gi, drop[j]);
  }
  for (let i = 0; i < nd; i++) {
    const gi = drop[i];
    const rowD = i * nd;
    for (let j = 0; j < nd; j++) D[rowD + j] = packedUpperGet(des.packed, n, gi, drop[j]);
  }

  choleskyLowerInPlace(D, nd);
  const X = new Float64Array(nd * nk);
  for (let col = 0; col < nk; col++) {
    const rhs = new Float64Array(nd);
    for (let i = 0; i < nd; i++) rhs[i] = B[col * nd + i];
    const y = solveLowerInPlace(D, nd, rhs);
    const x = solveUpperFromLowerTransposeInPlace(D, nd, y);
    for (let i = 0; i < nd; i++) X[i * nk + col] = x[i];
  }

  const precision = new Float64Array(nk * nk);
  for (let i = 0; i < nk; i++) {
    const rowP = i * nk;
    const rowA = i * nk;
    const rowB = i * nd;
    for (let j = 0; j < nk; j++) {
      let s = A[rowA + j];
      for (let k = 0; k < nd; k++) s -= B[rowB + k] * X[k * nk + j];
      precision[rowP + j] = s;
    }
  }
  for (let i = 0; i < nk; i++) {
    const row = i * nk;
    for (let j = 0; j < i; j++) {
      const s = 0.5 * (precision[row + j] + precision[j * nk + i]);
      precision[row + j] = s;
      precision[j * nk + i] = s;
    }
  }
  return precision;
}

function buildModelArray(z, fn) {
  const out = new Float64Array(z.length);
  for (let i = 0; i < z.length; i++) out[i] = fn(z[i]);
  return out;
}

async function main() {
  const pantheon = await readPantheon();
  const pCov = new Float64Array(pantheon.covariance);
  console.error(`pantheon rows kept ${pantheon.nKeep}`);
  choleskyLowerInPlace(pCov, pantheon.nKeep);
  const pFull = profileFromCholesky(pCov, pantheon.nKeep, pantheon.observed, buildModelArray(pantheon.z, modelFullScreen));
  const pDeleted = profileFromCholesky(pCov, pantheon.nKeep, pantheon.observed, buildModelArray(pantheon.z, modelDeletedScreen));
  const pDuplicated = profileFromCholesky(pCov, pantheon.nKeep, pantheon.observed, buildModelArray(pantheon.z, modelDuplicatedScreen));
  const pWrong = profileFromCholesky(pCov, pantheon.nKeep, pantheon.observed, buildModelArray(pantheon.z, modelWrongTransfer));

  const des = await readDes();
  console.error(`des rows kept ${des.nKeep} of ${des.nAll}`);
  const dPrecision = buildDesMarginalPrecision(des);
  const dFull = profileFromPrecision(dPrecision, des.nKeep, des.observed, buildModelArray(des.z, modelFullScreen));
  const dDeleted = profileFromPrecision(dPrecision, des.nKeep, des.observed, buildModelArray(des.z, modelDeletedScreen));
  const dDuplicated = profileFromPrecision(dPrecision, des.nKeep, des.observed, buildModelArray(des.z, modelDuplicatedScreen));
  const dWrong = profileFromPrecision(dPrecision, des.nKeep, des.observed, buildModelArray(des.z, modelWrongTransfer));

  const result = {
    pantheon: {
      n: pantheon.nKeep,
      chi2: pFull.chi2,
      offset: pFull.offset,
      deleted: pDeleted.chi2,
      duplicated: pDuplicated.chi2,
      wrongTransfer: pWrong.chi2,
    },
    des: {
      n: des.nKeep,
      chi2: dFull.chi2,
      offset: dFull.offset,
      deleted: dDeleted.chi2,
      duplicated: dDuplicated.chi2,
      wrongTransfer: dWrong.chi2,
    },
  };
  const reference = JSON.parse(
    fs.readFileSync(path.join(__dirname, 'PRODUCTION_RESULT.json'), 'utf8')
  );
  const checks = {
    pantheonCount: result.pantheon.n === reference.pantheon.n_data,
    desCount: result.des.n === reference.des.n_data,
    pantheonChi2: Math.abs(result.pantheon.chi2 - reference.pantheon.chi2) <= 3e-6,
    pantheonOffset: Math.abs(result.pantheon.offset - reference.pantheon.offset_B) <= 3e-9,
    desChi2: Math.abs(result.des.chi2 - reference.des.chi2) <= 3e-6,
    desOffset: Math.abs(result.des.offset - reference.des.offset_B) <= 3e-9,
    pantheonDeletedCaught: result.pantheon.deleted > result.pantheon.chi2 + 100.0,
    pantheonDuplicatedCaught: result.pantheon.duplicated > result.pantheon.chi2 + 100.0,
    pantheonWrongTransferCaught: result.pantheon.wrongTransfer > result.pantheon.chi2 + 100.0,
    desDeletedCaught: result.des.deleted > result.des.chi2 + 100.0,
    desDuplicatedCaught: result.des.duplicated > result.des.chi2 + 100.0,
    desWrongTransferCaught: result.des.wrongTransfer > result.des.chi2 + 100.0,
  };
  result.audit = 'G185_SEALED_DEPENDENCY_FREE_REPLAY';
  result.status = Object.values(checks).every(Boolean) ? 'PASS' : 'FAIL';
  result.checks = checks;
  console.log(JSON.stringify(result, null, 2));
  if (result.status !== 'PASS') process.exit(1);
}

main().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});
