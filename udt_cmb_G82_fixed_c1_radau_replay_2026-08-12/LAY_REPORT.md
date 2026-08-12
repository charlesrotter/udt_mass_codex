# G82 lay report

We reran the same tilted-light-ray test using a different kind of numerical engine.

The earlier calculations used DOP853. G82 used Radau, which advances the equations in a materially
different way. Nothing about the universe model, ray, endpoints, or measuring screens was changed.

The two engines produced essentially the same answer: their screen-distortion matrices differ by
less than one part in one hundred billion. The forward/reverse and rotated-screen rules still pass.

In the camera metaphor, we did not take a new photograph. We developed the same exposure using a
different processing machine and obtained the same geometry.

This removes one numerical concern. It does not choose the real cosmic profile or `X_max`, and it
does not yet create a CMB prediction. External review is the remaining evidence gate before this
small support result is fully banked.
