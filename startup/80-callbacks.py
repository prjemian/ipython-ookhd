print(__file__)

# custom callbacks

import APS_BlueSky_tools.callbacks

doc_collector = APS_BlueSky_tools.callbacks.DocumentCollectorCallback()
callback_db['doc_collector'] = RE.subscribe(doc_collector)
