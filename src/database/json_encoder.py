import dataclasses

import json


class EnhancedJSONEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        
        return super().default(obj)

