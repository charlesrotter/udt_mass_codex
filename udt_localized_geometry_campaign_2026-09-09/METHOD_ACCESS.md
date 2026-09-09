# Public mathematical methods — access and ownership

Sources are mathematical methods, not UDT premises. Primary versions:

- Chrusciel--Isenberg--Pollack, gr-qc/0403066v2,16June2005,
  https://arxiv.org/pdf/gr-qc/0403066v2 : section1 KID/development correspondence.
  Browser read; full PDF bytes not pinned by parent. Its no-KID/topology-changing
  theorem is NOT applied to this task.
- Chrusciel--Delay, gr-qc/0301073v2,11July2003,
  https://arxiv.org/pdf/gr-qc/0301073v2 : projected local constraint method.
  Parent read section2, relevant section3 projection/inverse/regularity results,
  Theorem5.9/Proposition5.10/Corollary5.11 and the section8 symmetry-uniqueness
  application. This is not a review of every result in the87-page paper.

The browser's source rendering and one PDF screenshot fetch were insufficient
for a typography check (one screenshot returned cache miss). Sandbox curl
could not resolve arxiv.org; the approved network retry succeeded. Exact command:

    curl --fail --location --max-time 60 --output /tmp/udt-lg-method-LvEXhm/chrusciel_delay_gr-qc-0301073v2.pdf https://arxiv.org/pdf/gr-qc/0301073v2

Downloaded PDF SHA256:
953f003fe179d5f686284b5755fcd4df381d3bbd3e9897bc11605650f3832dbb
Parent inspected printed pp25--27 with pdftotext22.02.0:

    pdftotext -layout -f 25 -l 27 /tmp/udt-lg-method-LvEXhm/chrusciel_delay_gr-qc-0301073v2.pdf -

LG2's psi=exp(-sigma/d) names the factor in the section3 variational correction;
the error/correction decay-space labels have the positive exponential. The
displayed theorem's exp(-2sigma/d) correction and exp(+2sigma/d) projected
residual are retained. These roles must not be conflated when defining the
weighted reference kernel. No source equation was edited. The fresh reviewer
independently identified the same distinction before reading LG2.

The smooth local evolution method remains explicitly conditional as in
G303/G315, with G321's hypothesis-interface discipline. Smooth compact support
is not analyticity. No imported method is claimed as native physical law or
as machine-proved by the symbolic checks. Temporary downloads are not required
repository artifacts; source URL/version/hash permit identification.
