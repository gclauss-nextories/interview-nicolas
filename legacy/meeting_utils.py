import re
import user_agents

from .geo_utils import distance_between_departments

from .models import CustomerSettings, MovingProject, Partner

PARTNER_ACCOUNT_GDPUBLIC_ID = "00000000-0000-0000-0000-000000000001"
PARTNER_ACCOUNT_GDPUBLIC_NOARRHES_ID = "00000000-0000-0000-0000-000000000002"

# PARAMETERS
AVAILABLE_VAD_POSTALS = ['75', '77', '78', '91', '92', '93', '94', '95']
AVAILABLE_VISIO_TEL_POSTALS = ['33', '31', '69', '13', '06', '83', '01',
                               '38', '42', '30', '80', '02',
                               '67', '68', '60', '28', '24', '47', '40',
                               '16', '17', '32', '82', '81', '65', '09',
                               '22', '29', '56', '44', '35', '27',
                               '14', '76',
                               '54', '57',
                               '03', '63',
                               '45', '18',
                               '36', '37', '41', '71',
                               '07', '11', '26', '34', '84',
                               '59', '62',
                               '10', '51', '64', '66', '73', '74',
                               '85', '79', '49', '43', '25', '39', '90', '70', '55', '88', '08']

# AVAILABLE_VISIO_SPECIFICS = {
#     'versIDF': {
#         'chargement': ['*'],
#         'livraison': ['75', '77', '78', '91', '92', '93', '94', '95']
#     },
#     'versZonesDepart': {
#         'chargement': ['*'],
#         'livraison': ['27', '28', '60', '69', '42', '01', '33', '31', '13', '30', '06', '83', '34', '67', '68', '62',
#         '59', '22', '29', '56', '44', '35']
#     }
# }

# QUAND ESTIMATION, SURFACE ET VOLUME MINIMUM EN DESSOUS DESQUELS ON PROPOSE UNIQUEMENT UNE MER
VOLUME_MER_MIN = 30

SURFACE_MER_MIN = MovingProject.SURFACE_10
DISTANCE_MER_MIN = 300
SURFACE_MER_MAX = MovingProject.SURFACE_20
DISTANCE_MER_MAX = 100

# AU DEPART DE L'ILE-DE-FRANCE, LA MER S'ARRETE A 30 M2
SURFACE_MER_MAX_IDF = MovingProject.SURFACE_10

AVAILABLE_MER_POSTALS = [
    '75', '77', '78', '91', '92', '93', '94', '95',
    '33',
    '69',
    '13',
]

SURFACE_ONLINE_BOOKING = MovingProject.SURFACE_10

# QUAND ESTIMATION, SURFACE ET VOLUME MINIMUM EN DESSOUS DESQUELS ON NE PROPOSE PAS DE VAD
VOLUME_VAD_MIN = 20
SURFACE_ESTIM_VAD_MIN = MovingProject.SURFACE_20

# QUAND PAS D'ESTIMATION, ON NE PROPOSE PAS LA VAD SI SURFACE FAIBLE
SURFACE_NOESTIM_VAD_MIN = MovingProject.SURFACE_10


# ADD ONE SAFE FOR LOWEST VALUE OF A RANGE TO EXCLUDE IT FROM NEXT RANGE
# Ex: 30-50 becomes 31 which is > 30 (<30 becomes 30 with get_max)
def surfaceToInt(surface, get_max=False, add_one_safe=False):
    if surface is None or surface == MovingProject.SURFACE_10:
        return 30 if get_max else 0
    delim = surface.find('-')
    one_safe = 0
    if delim > 0:
        surface = surface[delim + 1:] if get_max else surface[:delim]
        if add_one_safe and not get_max:
            one_safe = 1
    surface = re.sub("[^0-9]", "", surface)
    return int(surface) + one_safe


def intToSurface(surface):
    try:
        surface = int(surface)
        if surface < 30:
            return MovingProject.SURFACE_10
        if surface < 50:
            return MovingProject.SURFACE_20
        if surface < 80:
            return MovingProject.SURFACE_30
        if surface < 120:
            return MovingProject.SURFACE_50
        if surface < 180:
            return MovingProject.SURFACE_100
        return MovingProject.SURFACE_100_PLUS
    except:
        return None


def getRdvDuration(surface, est_volume):
    duration = 45
    if surface == MovingProject.SURFACE_100_PLUS:
        duration = 90
    if surface == MovingProject.SURFACE_100:
        duration = 75
    if surface == MovingProject.SURFACE_50:
        duration = 60

    surface_int = surfaceToInt(surface) + 20
    if est_volume:
        if est_volume > int(surface_int / 2):
            duration += 15
        if est_volume < int(surface_int / 3):
            duration -= 15

    return max(duration, 45)


def isIleDeFrance(postal_code):
    return postal_code in ['75', '77', '78', '91', '92', '93', '94', '95']


def isDemenagementLocal(dep_postal_code, arr_postal_code):
    return dep_postal_code == arr_postal_code or (isIleDeFrance(dep_postal_code) and isIleDeFrance(arr_postal_code))


def isB2BPartner(partner: Partner):
    return partner.default_handling_type == "HANDLING_TYPE_COMMISSIONNAIRE" \
        and partner.default_partner_account_id not in [
            PARTNER_ACCOUNT_GDPUBLIC_ID,
            PARTNER_ACCOUNT_GDPUBLIC_NOARRHES_ID
        ]


def disallow_partner_lead_sell(partner: Partner, is_N1_action=False):
    if is_N1_action:
        return partner.disallow_manual_lead_sell
    return partner.always_import


def is_mer_available(
    dep_postal_code,
    arr_postal_code,
    surfaceInt,
    volume,
    from_country=None,
    to_country=None,
    allow_all_small_distances=False
):
    # REMOVE INTERNATIONAL MOVES
    if (from_country is not None and from_country != 'FR') \
       or (to_country is not None and to_country != 'FR'):
        return False
    if dep_postal_code not in AVAILABLE_MER_POSTALS:
        return False
    try:
        # TODO handle international (postal code is not int but string)
        approx_distance = distance_between_departments(int(dep_postal_code), int(arr_postal_code))
    except ValueError:
        return False
    if approx_distance is not None:
        if allow_all_small_distances and approx_distance < DISTANCE_MER_MAX:
            return True
        if surfaceInt <= surfaceToInt(SURFACE_MER_MIN, get_max=True):
            return approx_distance < DISTANCE_MER_MIN
        surface_max = SURFACE_MER_MAX_IDF if isIleDeFrance(dep_postal_code) else SURFACE_MER_MAX
        if surfaceInt <= surfaceToInt(surface_max, get_max=True):
            return approx_distance < DISTANCE_MER_MAX
    return False


def isMeettypeAvailable(meettype, dep_postal_code, arr_postal_code, surface, volume,
                        partner=None, from_country=None, to_country=None, request=None, 
                        bypass_optimize=False, is_N1_action=False):
    # Disabled OnlineBooking for users IE11 or users not in France
    if meettype == MovingProject.MEETTYPE_ONLINE:
        if (from_country is not None and from_country != 'FR') \
                or (to_country is not None and to_country != 'FR'):
            return False
        if request:
            try:
                user_agent = user_agents.parse(request.META['HTTP_USER_AGENT'])
                if user_agent.browser.family == 'IE' and user_agent.browser.version[0] <= 11:
                    return False
            except:
                pass
    # SPECIAL CASE FOR PARTNERS
    if partner and (
        isB2BPartner(partner)
        or disallow_partner_lead_sell(partner, is_N1_action)
    ):
        if meettype in [MovingProject.MEETTYPE_MER, MovingProject.MEETTYPE_ONLINE]:
            return False
        if meettype in [MovingProject.MEETTYPE_VISIO, MovingProject.MEETTYPE_TEL]:
            return True

    # FROM INTERNATIONAL TO INTERNATIONAL
    if (from_country is not None and from_country != 'FR') \
            and (to_country is not None and to_country != 'FR'):
        return meettype == MovingProject.MEETTYPE_MER

    if not dep_postal_code:
        return meettype not in [MovingProject.MEETTYPE_MER, MovingProject.MEETTYPE_ONLINE, MovingProject.MEETTYPE_VAD]

    if len(dep_postal_code) > 2:
        dep_postal_code = dep_postal_code[:2]

    try:
        int(dep_postal_code)
    except ValueError:
        return meettype not in [MovingProject.MEETTYPE_MER, MovingProject.MEETTYPE_ONLINE, MovingProject.MEETTYPE_VAD]

    # CHECK IF THE PROJECT IS BIG ENOUGH
    surfaceInt = surfaceToInt(surface, add_one_safe=True)
    is_local_moving = True
    force_no_vad = False

    if arr_postal_code:
        if len(arr_postal_code) > 2:
            arr_postal_code = arr_postal_code[:2]

        if is_mer_available(dep_postal_code,
                            arr_postal_code,
                            surfaceInt,
                            volume,
                            from_country,
                            to_country,
                            allow_all_small_distances=is_N1_action):
            allow_leads = CustomerSettings.get_setting_value(CustomerSettings.SETTING_ALLOW_LEADS)
            if allow_leads:
                return meettype == MovingProject.MEETTYPE_MER

        is_local_moving = isDemenagementLocal(dep_postal_code, arr_postal_code)

        # ESTIM WITH SMALL VOLUME AND SMALL SURFACE => DONT LET USERS CHOOSE VAD
        if is_local_moving and volume and volume <= VOLUME_VAD_MIN \
           and surfaceInt <= surfaceToInt(SURFACE_ESTIM_VAD_MIN, get_max=True):
            force_no_vad = True

    allow_online = allowOnlineBooking(volume, surfaceInt, is_local_moving, request, bypass_optimize)
    force_no_vad = allow_online or force_no_vad

    if dep_postal_code in AVAILABLE_VAD_POSTALS:
        return meettype != MovingProject.MEETTYPE_MER \
            and (not force_no_vad or meettype != MovingProject.MEETTYPE_VAD) \
            and (allow_online or meettype != MovingProject.MEETTYPE_ONLINE)

    return meettype not in [MovingProject.MEETTYPE_MER, MovingProject.MEETTYPE_VAD] \
        and (allow_online or meettype != MovingProject.MEETTYPE_ONLINE)


def isIDemenagerAvailable(dep_postal_code, arr_postal_code, surface, volume, partner=None):
    return not isMeettypeAvailable(MovingProject.MEETTYPE_MER, dep_postal_code, arr_postal_code, surface, volume,
                                   partner)


def isMERBecauseOfZone(dep_postal_code, arr_postal_code):
    return not isIDemenagerAvailable(dep_postal_code, arr_postal_code, MovingProject.SURFACE_100_PLUS,
                                     VOLUME_MER_MIN + 1)


def allowOnlineBooking(volume, surfaceInt, is_local_moving, request, bypass_optimize):
    # DONT ALLOW ONLINE BOOKING WITH AN ESTIMATION
    if volume is not None:
        return False
    if surfaceInt <= surfaceToInt(SURFACE_ONLINE_BOOKING, get_max=True):
        # experiment_value = get_online_booking_experiment_variant(request)
        # return bypass_optimize or experiment_value == 1
        return True
    return False


def getPostalFromAddress(address):
    if not address:
        return None
    p = re.search("^(\\d{5})$|^(\\d{5})\\D|\\D(\\d{5})$|\\D(\\d{5})\\D", address)
    if p:
        for m in p.groups():
            if m:
                return m
    return None
