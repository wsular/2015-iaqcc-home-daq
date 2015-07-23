*Datalogger Program Source Code*

Sensors are wired to a CR3000 as specified in `wiring.docx` ([PDF version][1]).

  [1]: https://bitbucket.org/wsular/2015-iaq-intensive-daq/downloads/interior-daq-wiring.pdf

1. Edit values in `scadabr-template.cr3` and save as `scadabr.cr3` then save and 
   encrypt to `scadabr_Enc.cr3`. Load `scadabr_Enc.cr3` onto the CR3000's `CPU:`
   drive.
2. Repeat pattern in step 1 for `email-template.cr3`.
3. Load `default.cr3` onto the CR3000's `CPU:` drive.
