TERMS = ['Terms of use must be accepted']
EMAIL = ['Email address not entered',
         'Invalid email address format',
         'Email address does not exist',
         'Email address already exist in the database']

PASSWORD = ['Password not entered',
            'Non-alphanumeric password',
            'Invalid password entered',
            'Temporary password emailed']

PASSWORD_REPEAT = ['Repeat password not entered',
                   'Non-alphanumeric repeat password entered',
                   'Entered passwords do not match',
                   'Password changed']

PASSWORD_OLD = ['Old password not entered',
                'Non-alphanumeric old password entered']

PASSWORD_NEW = ['New password not entered',
                'Non-alphanumeric new password entered']

STORE_NAME = ['Store name not entered',
              'Non-alphanumeric storename entered',
              'Restricted storename entered',
              'Storename taken',
              'Storename must be between 5 and 18 characters long']

BITCOIN_ADDRESS = ['Bitcoin address not entered',
                   'Invalid bitcoin address format']

SIGNATURE = ['Signature not entered',
             'Invalid signature format',
             'Message was not verified']

FIRST = ['First name not entered',
         'Non-alphanumeric first name entered']

LAST = ['Last name not entered',
        'Non-alphanumeric last name entered']

#MESSAGE
NAME = ['Sender name not entered',
        'Non-alphanumeric sender name entered']

SUBJECT = ['Message subject not entered',
           'Invalid subject format entered']

BODY = ['Message body not entered',
        'Invalid body format entered']

REGEX_NAME = '^[\w\s-]+$'
REGEX_SUBJECT = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_BODY = "^[\w'*$&!?,.;:()/\s-]+$"
MESSAGE_SUCCESS = "Your message has been sent."

#REVIEW
REVIEW_SUCCESS = "Your review has been submitted. Thank you!"

ADDRESS1 = ['Street address1 not entered',
            'Invalid street address1 format',
            'Address saved']

ADDRESS2 = ['Street address2 not entered',
            'Invalid street address2 format']

CITY = ['City not entered',
        'Non-alphanumeric city entered']

STATE = ['State not entered',
         'Non-alphanumeric state entered']

ZIP = ['Zip not entered',
       'Invalid zip format entered']

PHONE = ['Phone number not entered',
         'Invalid phone number entered']

NOTE = ['Phone number not entered',
        "Invalid note format entered ( letters, numbers and. ? ! : ; - ( ) ' / ,  & $ * . , ! only )"]

QUANTITY = ['Quantity not entered',
            'Non-numeric quantity entered',
            'Quantity cannot be negative',
            'Not Enough Stock Available',
            'Quantity Updated']

UNDEF = 'Undef error message'


#PRODUCT
TITLE = ['Title not entered',
         "Invalid name format entered ( letters, numbers and. ? ! : ; - ( ) ' / ,  & $ * . , ! only )"]

DESCRIPTION = ['Description not entered',
               "Invalid description format entered ( letters, numbers and. ? ! : ; - ( ) ' / ,  & $ * . , ! only )",
               'Description must be between 5 and 2000 characters long']

PRICE = ['Price not entered',
         'Price must be numeric',
         'Price must be greated than 0']

STOCK = ['Stock value not entered',
         'Stock value must be greater than 0',
         'Stock value must be an integer']

COUNTRIES = ['Shipping destination not selected',
             'Shipping cost must be numeric']


STORE_DESCRIPTION = ['Description must be between 5 and 200 characters long']

NULL_IMAGE = 'images/products/no-image'
NULL_LOGO = 'images/stores/no-image'


REVIEW_HEADLINE = ['Review headline not entered',
                   'Invalid review headline format']

REVIEW_BODY = ['Review body not entered']

MESSAGE_SUBJECT = ['Message subject not entered',
                   'Invalid message subject format']

MESSAGE_BODY = ['Message body not entered']

INVALID_QUERY = 'Non-alphanumeric search query entered'
INVALID_SHIPPING = 'Invalid shipping rate entered'
INVALID_VENDOR_TOKEN = 'Invalid user token entered'
OK_RESPONSE = "OK"

SUCCESS_LOGIN = "Login successful!"
VERIFY_SUCCESS = "Email successfully verified"
UPDATE_SUCCESS = "Information saved"
CLOSE_SUCCESS = "Store closed successfully"

REGEX_QUERY = '^[\w-]+$'
REGEX_BITCOIN_ADDRESS = '^[\w-]+$'
REGEX_EMAIL = '^[^@ ]+@[^@ ]+\.[^@ ]+$'
REGEX_PASSWORD = '^[\w-]+$'
REGEX_PHONE = '^[\w-]*$'
#REGEX_REVIEW_HEADLINE = '^[\w\s-]+$'
REGEX_REVIEW_HEADLINE = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_MESSAGE_SUBJECT = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_MESSAGE_BODY = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_DESCRIPTION = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_NOTE = "^[\w'*$&!?,.;:()/\s-]*$"
REGEX_TITLE = "^[\w'*$&!?,.;:()/\s-]+$"
REGEX_STORENAME = '^[\w-]+$'
REGEX_TOKEN = '^[\w-]+$'
REGEX_FIRST = '^[\w\s-]+$'
REGEX_LAST = '^[\w\s-]+$'
REGEX_STREET_ADDRESS_1 = '^[\w\s-]+$'
REGEX_STREET_ADDRESS_2 = '^[\w\s-]*$'
REGEX_CITY = '^[\w\s-]+$'
REGEX_STATE = '^[\w\s-]+$'
REGEX_ZIP = '^[\w-]+$'
REGEX_COUNTRY = '^[\w-]+$'

currencies = ['USD',
              'AUD',
              'CHF',
              'RUB',
              'SEK',
              'THB',
              'CNY',
              'JPY',
              'GBP',
              'NZD',
              'PLN',
              'EUR',
              'DKK',
              'SGD',
              'HKD',
              'CAD']

productCategories = {'ZZ': 'All Categories',
                     'AA': 'Automotive & Industrial',
                     'AB': 'Books',
                     'AC': 'Clothing, Shoes & Jewelry',
                     'AD': 'Electronics & Office',
                     'AE': 'Grocery, Health & Beauty',
                     'AF': 'Home, Garden & Tools',
                     'AG': 'Miscellaneous',
                     'AH': 'Movies, Music & Games',
                     'AI': 'Pets',
                     'AJ': 'Sports & Outdoors',
                     'AK': 'Toys, Kids & Baby',
                     'AL': 'Art & Collectibles'}

shippingCarriers = {'AA': 'DHL',
                    'AB': 'Fedex',
                    'AC': 'UPS',
                    'AD': 'UPS Mail Innovations',
                    'AE': 'USPS',
                    'AF': 'Other'}

orderCancelationReasons = {'AA': 'Order not paid within 24 hours of placement',
                           'AB': 'Fraudulent customer information provided',
                           'AC': 'Buyer refund granted',
                           'AD': 'Payment address fault'}

carriers = ['DHL',
            'Fedex',
            'UPS',
            'UPS Mail Innovations',
            'USPS',
            'Other']


questions = ['Was description of the item accurate?',
             'Did seller ship the item quickly?',
             'Was price of the item fair?',
             'Were shipping and handling charges reasonable?',
             'Would you buy from the seller again?']

restrictedStoreNames = ['addressBook',
                        'buyPhysical',
                        'buyer',
                        'cancel',
                        'category',
                        'checkoutDigital',
                        'checkoutPhysical',
                        'createBuyer',
                        'createSeller',
                        'disconnect',
                        'deleteAddress',
                        'deletePhysical',
                        'deleteProduct',
                        'deleteUser',
                        'faq',
                        'getSessionUser',
                        'images',
                        'invoice',
                        'loadAddress',
                        'loadCountries',
                        'loadRating',
                        'login',
                        'loginAction',
                        'logout',
                        'orders',
                        'orders',
                        'policy',
                        'promoteAddress',
                        'receipt',
                        'resetAddress',
                        'recoverPassword',
                        'saveAddress',
                        'saveBuyerInfo',
                        'savePassword',
                        'savePaymentStatus',
                        'savePhysical',
                        'saveSellerInfo',
                        'saveUser',
                        'saveQuantity',
                        'saveReview',
                        'saveStore',
                        'saveTrackingNumber',
                        'scripts',
                        'searchAction',
                        'seller',
                        'sendToken',
                        'settings',
                        'styles',
                        'summaryOrders',
                        'summaryPayments',
                        'summaryProducts',
                        'summarySessions',
                        'summaryUsers',
                        'terms',
                        'verifyDetailsDigital',
                        'verifyDetailsPhysical',
                        'verifyToken']
#%s/, .*/

accountTypes = ['admin',
                'buyer',
                'seller']

paymentStatuses = ['Not paid',
                   'Paid']

shippingStatuses = ['Not shipped',
                    'Shipped']


countries = ['Afghanistan',
             'Albania',
             'Algeria',
             'Andorra',
             'Angola',
             'Antigua and Deps',
             'Argentina',
             'Armenia',
             'Australia',
             'Austria',
             'Azerbaijan',
             'Bahamas',
             'Bahrain',
             'Bangladesh',
             'Barbados',
             'Belarus',
             'Belgium',
             'Belize',
             'Benin',
             'Bhutan',
             'Bolivia',
             'Bosnia Herzegovina',
             'Botswana',
             'Brazil',
             'Brunei',
             'Bulgaria',
             'Burkina',
             'Burundi',
             'Cambodia',
             'Cameroon',
             'Canada',
             'Cape Verde',
             'Central African Rep',
             'Chad',
             'Chile',
             'China',
             'Colombia',
             'Comoros',
             'Congo',
             'Congo (Democratic Rep)',
             'Costa Rica',
             'Croatia',
             'Cuba',
             'Cyprus',
             'Czech Republic',
             'Denmark',
             'Djibouti',
             'Dominica',
             'Dominican Republic',
             'East Timor',
             'Ecuador',
             'Egypt',
             'El Salvador',
             'Equatorial Guinea',
             'Eritrea',
             'Estonia',
             'Ethiopia',
             'Fiji',
             'Finland',
             'France',
             'Gabon',
             'Gambia',
             'Georgia',
             'Germany',
             'Ghana',
             'Greece',
             'Grenada',
             'Guatemala',
             'Guinea',
             'Guinea-Bissau',
             'Guyana',
             'Haiti',
             'Honduras',
             'Hungary',
             'Iceland',
             'India',
             'Indonesia',
             'Iran',
             'Iraq',
             'Ireland (Republic)',
             'Israel',
             'Italy',
             'Ivory Coast',
             'Jamaica',
             'Japan',
             'Jordan',
             'Kazakhstan',
             'Kenya',
             'Kiribati',
             'Korea North',
             'Korea South',
             'Kosovo',
             'Kuwait',
             'Kyrgyzstan',
             'Laos',
             'Latvia',
             'Lebanon',
             'Lesotho',
             'Liberia',
             'Libya',
             'Liechtenstein',
             'Lithuania',
             'Luxembourg',
             'Macedonia',
             'Madagascar',
             'Malawi',
             'Malaysia',
             'Maldives',
             'Mali',
             'Malta',
             'Marshall Islands',
             'Mauritania',
             'Mauritius',
             'Mexico',
             'Micronesia',
             'Moldova',
             'Monaco',
             'Mongolia',
             'Montenegro',
             'Morocco',
             'Mozambique',
             'Myanmar (Burma)',
             'Namibia',
             'Nauru',
             'Nepal',
             'Netherlands',
             'New Zealand',
             'Nicaragua',
             'Niger',
             'Nigeria',
             'Norway',
             'Oman',
             'Pakistan',
             'Palau',
             'Panama',
             'Papua New Guinea',
             'Paraguay',
             'Peru',
             'Philippines',
             'Poland',
             'Portugal',
             'Qatar',
             'Romania',
             'Russian Federation',
             'Rwanda',
             'St Kitts and Nevis',
             'St Lucia',
             'Saint Vincent and the Grenadines',
             'Samoa',
             'San Marino',
             'Sao Tome and Principe',
             'Saudi Arabia',
             'Senegal',
             'Serbia',
             'Seychelles',
             'Sierra Leone',
             'Singapore',
             'Slovakia',
             'Slovenia',
             'Solomon Islands',
             'Somalia',
             'South Africa',
             'South Sudan',
             'Spain',
             'Sri Lanka',
             'Sudan',
             'Suriname',
             'Swaziland',
             'Sweden',
             'Switzerland',
             'Syria',
             'Taiwan',
             'Tajikistan',
             'Tanzania',
             'Thailand',
             'Togo',
             'Tonga',
             'Trinidad and Tobago',
             'Tunisia',
             'Turkey',
             'Turkmenistan',
             'Tuvalu',
             'Uganda',
             'Ukraine',
             'United Arab Emirates',
             'United Kingdom',
             'United States',
             'Uruguay',
             'Uzbekistan',
             'Vanuatu',
             'Vatican City',
             'Venezuela',
             'Vietnam',
             'Yemen',
             'Zambia',
             'Zimbabwe']
