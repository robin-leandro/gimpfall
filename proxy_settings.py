from gimpfu import PF_FLOAT, PF_FILE, PF_BOOL
def get_default_settings():
    i = [-1]
    def inc():
        i[0]+=1
        return i[0] 
    return {
        'sheet_width_in': {
            'type': PF_FLOAT, 
            'name':'sheet_width_in', 
            'description':'Width in inches:', 
            'value':19, 
            'order':inc()
        },
        'sheet_height_in': {
            'type': PF_FLOAT, 
            'name': 'sheet_height_in', 
            'description':'Height in inches:', 
            'value':13, 
            'order':inc()
        },
        'card_width_cm': {
            'type': PF_FLOAT, 
            'name': 'card_width_cm', 
            'description':'Width of each card in centimeters:', 
            'value': 6.3, 
            'order':inc()
        },
        'card_height_px': {
            'type': PF_FLOAT, 
            'name': 'card_height_cm', 
            'description':'Height of each card in centimeters:', 
            'value':8.8, 
            'order':inc()
        },
        'cardback_path': {
            'type': PF_FILE, 
            'name': 'cardback_path', 
            'description':'Path to the cardback to use:', 
            'value':'', 
            'order':inc()
        },
        'greyscale': {
            'type': PF_BOOL, 
            'name': 'greyscale', 
            'description':'Greyscale images?', 
            'value':False, 
            'order':inc()
        },
        'fix_eighth_in_margin': {
            'type': PF_BOOL, 
            'name': 'fix_eighth_in_margin', 
            'description':'Fix 1/8th inch margin?', 
            'value':False, 
            'order':inc()
        },
        'evenly_space_cards': {
            'type': PF_BOOL, 
            'name': 'evenly_space_cards', 
            'description':'Leave even spaces between cards?', 
            'value':True, 
            'order':inc()
        },
        'cardback_scale_percent': {
            'type': PF_FLOAT,
            'name': 'cardback_scale_percent', 
            'description':'Percent to enlarge cardbacks as compared to front faces (evenly_space_cards must be true if <0):', 
            'value':1.5, 
            'order':inc()
        }
    }

def settings_map_to_gimp_tuple(settings):
    return map(lambda s: (s['type'], s['name'], s['description'], s['value']), sorted(settings.values(), key = lambda s: s['order']))

class ProxySettings:
    settings = get_default_settings()

    def __init__(self, *args):
        for setting in self.settings.keys():
            self.settings[setting]['value'] = args[0][self.settings[setting]['order']]

    def get(self, name):
        return self.settings[name]['value']
    
    def get_all(self):
        return tuple(map(lambda s: s['value'], sorted(self.settings.values(), key= lambda s: s['order'])))



































