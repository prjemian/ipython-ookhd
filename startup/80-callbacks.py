print(__file__)

# custom callbacks

import APS_BlueSky_tools.callbacks
import APS_BlueSky_tools.filewriters

doc_collector = APS_BlueSky_tools.callbacks.DocumentCollectorCallback()
callback_db['doc_collector'] = RE.subscribe(doc_collector.receiver)

specwriter = APS_BlueSky_tools.filewriters.SpecWriterCallback()
callback_db['specwriter'] = RE.subscribe(specwriter.receiver)
# for developer, write the SPEC file to /tmp (assumes OS is Linux)
specwriter.newfile(os.path.join("/tmp", specwriter.spec_filename))
print("SPEC data file:", specwriter.spec_filename)
