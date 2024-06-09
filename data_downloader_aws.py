import os
import requests
import boto3


# Base URL
base_url = "https://cycling.data.tfl.gov.uk/usage-stats/"

# List of file names to download, copy and pasted from output of csv_to_names_to_download.ipynb
file_names = ['01aJourneyDataExtract10Jan16-23Jan16.csv',
                '01b%20Journey%20Data%20Extract%2024Jan16-06Feb16.csv',
                '01bJourneyDataExtract24Jan16-06Feb16.csv',
                '02aJourneyDataExtract07Fe16-20Feb2016.csv',
                '02bJourneyDataExtract21Feb16-05Mar2016.csv',
                '03JourneyDataExtract06Mar2016-31Mar2016.csv',
                '04JourneyDataExtract01Apr2016-30Apr2016.csv',
                '05JourneyDataExtract01May2016-17May2016.csv',
                '06JourneyDataExtract18May2016-24May2016.csv',
                '07JourneyDataExtract25May2016-31May2016.csv',
                '08JourneyDataExtract01Jun2016-07Jun2016.csv',
                '09JourneyDataExtract08Jun2016-14Jun2016.csv',
                '100JourneyDataExtract07Mar2018-13Mar2018.csv',
                '101JourneyDataExtract14Mar2018-20Mar2018.csv',
                '102JourneyDataExtract21Mar2018-27Mar2018.csv',
                '103JourneyDataExtract28Mar2018-03Apr2018.csv',
                '104JourneyDataExtract04Apr2018-10Apr2018.csv',
                '105JourneyDataExtract11Apr2018-17Apr2018.csv',
                '106JourneyDataExtract18Apr2018-24Apr2018.csv',
                '107JourneyDataExtract25Apr2018-01May2018.csv',
                '108JourneyDataExtract02May2018-08May2018.csv',
                '109JourneyDataExtract09May2018-15May2018.csv',
                '10JourneyDataExtract15Jun2016-21Jun2016.csv',
                '10a-Journey-Data-Extract-20Sep15-03Oct15.csv',
                '10b-Journey-Data-Extract-04Oct15-17Oct15.csv',
                '110JourneyDataExtract16May2018-22May2018.csv',
                '111JourneyDataExtract23May2018-29May2018.csv',
                '112JourneyDataExtract30May2018-05June2018.csv',
                '113JourneyDataExtract06June2018-12June2018.csv',
                '114JourneyDataExtract13June2018-19June2018.csv',
                '115JourneyDataExtract20June2018-26June2018.csv',
                '116JourneyDataExtract27June2018-03July2018.csv',
                '117JourneyDataExtract04July2018-10July2018.csv',
                '118JourneyDataExtract11July2018-17July2018.csv',
                '119JourneyDataExtract18July2018-24July2018.csv',
                '11JourneyDataExtract22Jun2016-28Jun2016.csv',
                '11a-Journey-Data-Extract-18Oct15-31Oct15.csv',
                '11b-Journey-Data-Extract-01Nov15-14Nov15.csv',
                '120JourneyDataExtract25July2018-31July2018.csv',
                '121JourneyDataExtract01Aug2018-07Aug2018.csv',
                '122JourneyDataExtract08Aug2018-14Aug2018.csv',
                '123JourneyDataExtract15Aug2018-21Aug2018.csv',
                '124JourneyDataExtract22Aug2018-28Aug2018.csv',
                '125JourneyDataExtract29Aug2018-04Sep2018.csv',
                '126JourneyDataExtract05Sep2018-11Sep2018.csv',
                '127JourneyDataExtract12Sep2018-18Sep2018.csv',
                '128JourneyDataExtract19Sep2018-25Sep2018.csv',
                '129JourneyDataExtract26Sep2018-02Oct2018.csv',
                '12JourneyDataExtract29Jun2016-05Jul2016.csv',
                '12aJourneyDataExtract15Nov15-27Nov15.csv',
                '12bJourneyDataExtract28Nov15-12Dec15.csv',
                '130JourneyDataExtract03Oct2018-09Oct2018.csv',
                '131JourneyDataExtract10Oct2018-16Oct2018.csv',
                '132JourneyDataExtract17Oct2018-23Oct2018.csv',
                '133JourneyDataExtract24Oct2018-30Oct2018.csv',
                '134JourneyDataExtract31Oct2018-06Nov2018.csv',
                '135JourneyDataExtract07Nov2018-13Nov2018.csv',
                '136JourneyDataExtract14Nov2018-20Nov2018.csv',
                '137JourneyDataExtract21Nov2018-27Nov2018.csv',
                '138JourneyDataExtract28Nov2018-04Dec2018.csv',
                '139JourneyDataExtract05Dec2018-11Dec2018.csv',
                '13JourneyDataExtract06Jul2016-12Jul2016.csv',
                '13aJourneyDataExtract13Dec15-24Dec15.csv',
                '13bJourneyDataExtract25Dec15-09Jan16.csv',
                '140JourneyDataExtract12Dec2018-18Dec2018.csv',
                '141JourneyDataExtract19Dec2018-25Dec2018.csv',
                '142JourneyDataExtract26Dec2018-01Jan2019.csv',
                '143JourneyDataExtract02Jan2019-08Jan2019.csv',
                '144JourneyDataExtract09Jan2019-15Jan2019.csv',
                '145JourneyDataExtract16Jan2019-22Jan2019.csv',
                '146JourneyDataExtract23Jan2019-29Jan2019.csv',
                '147JourneyDataExtract30Jan2019-05Feb2019.csv',
                '148JourneyDataExtract06Feb2019-12Feb2019.csv',
                '149JourneyDataExtract13Feb2019-19Feb2019.csv',
                '14JourneyDataExtract13Jul2016-19Jul2016.csv',
                '150JourneyDataExtract20Feb2019-26Feb2019.csv',
                '151JourneyDataExtract27Feb2019-05Mar2019.csv',
                '152JourneyDataExtract06Mar2019-12Mar2019.csv',
                '153JourneyDataExtract13Mar2019-19Mar2019.csv',
                '154JourneyDataExtract20Mar2019-26Mar2019.csv',
                '155JourneyDataExtract27Mar2019-02Apr2019.csv',
                '156JourneyDataExtract03Apr2019-09Apr2019.csv',
                '157JourneyDataExtract10Apr2019-16Apr2019.csv',
                '158JourneyDataExtract17Apr2019-23Apr2019.csv',
                '159JourneyDataExtract24Apr2019-30Apr2019.csv',
                '15JourneyDataExtract20Jul2016-26Jul2016.csv',
                '160JourneyDataExtract01May2019-07May2019.csv',
                '161JourneyDataExtract08May2019-14May2019.csv',
                '162JourneyDataExtract15May2019-21May2019.csv',
                '163JourneyDataExtract22May2019-28May2019.csv',
                '164JourneyDataExtract29May2019-04Jun2019.csv',
                '165JourneyDataExtract05Jun2019-11Jun2019.csv',
                '166JourneyDataExtract12Jun2019-18Jun2019.csv',
                '167JourneyDataExtract19Jun2019-25Jun2019.csv',
                '168JourneyDataExtract26Jun2019-02Jul2019.csv',
                '169JourneyDataExtract03Jul2019-09Jul2019.csv',
                '16JourneyDataExtract27Jul2016-02Aug2016.csv',
                '170JourneyDataExtract10Jul2019-16Jul2019.csv',
                '171JourneyDataExtract17Jul2019-23Jul2019.csv',
                '172JourneyDataExtract24Jul2019-30Jul2019.csv',
                '173JourneyDataExtract31Jul2019-06Aug2019.csv',
                '174JourneyDataExtract07Aug2019-13Aug2019.csv',
                '175JourneyDataExtract14Aug2019-20Aug2019.csv',
                '176JourneyDataExtract21Aug2019-27Aug2019.csv',
                '177JourneyDataExtract28Aug2019-03Sep2019.csv',
                '178JourneyDataExtract04Sep2019-10Sep2019.csv',
                '179JourneyDataExtract11Sep2019-17Sep2019.csv',
                '17JourneyDataExtract03Aug2016-09Aug2016.csv',
                '180JourneyDataExtract18Sep2019-24Sep2019.csv',
                '181JourneyDataExtract25Sep2019-01Oct2019.csv',
                '182JourneyDataExtract02Oct2019-08Oct2019.csv',
                '183JourneyDataExtract09Oct2019-15Oct2019.csv',
                '184JourneyDataExtract16Oct2019-22Oct2019.csv',
                '185JourneyDataExtract23Oct2019-29Oct2019.csv',
                '186JourneyDataExtract30Oct2019-05Nov2019.csv',
                '187JourneyDataExtract06Nov2019-12Nov2019.csv',
                '188JourneyDataExtract13Nov2019-19Nov2019.csv',
                '189JourneyDataExtract20Nov2019-26Nov2019.csv',
                '18JourneyDataExtract10Aug2016-16Aug2016.csv',
                '190JourneyDataExtract27Nov2019-03Dec2019.csv',
                '191JourneyDataExtract04Dec2019-10Dec2019.csv',
                '192JourneyDataExtract11Dec2019-17Dec2019.csv',
                '193JourneyDataExtract18Dec2019-24Dec2019.csv',
                '194JourneyDataExtract25Dec2019-31Dec2019.csv',
                '195JourneyDataExtract01Jan2020-07Jan2020.csv',
                '196JourneyDataExtract08Jan2020-14Jan2020.csv',
                '197JourneyDataExtract15Jan2020-21Jan2020.csv',
                '198JourneyDataExtract22Jan2020-28Jan2020.csv',
                '199JourneyDataExtract29Jan2020-04Feb2020.csv',
                '19JourneyDataExtract17Aug2016-23Aug2016.csv',
                '1a.JourneyDataExtract04Jan15-17Jan15.csv',
                '1b.JourneyDataExtract18Jan15-31Jan15.csv',
                '200JourneyDataExtract05Feb2020-11Feb2020.csv',
                '201JourneyDataExtract12Feb2020-18Feb2020.csv',
                '202JourneyDataExtract19Feb2020-25Feb2020.csv',
                '203JourneyDataExtract26Feb2020-03Mar2020.csv',
                '204JourneyDataExtract04Mar2020-10Mar2020.csv',
                '205JourneyDataExtract11Mar2020-17Mar2020.csv',
                '206JourneyDataExtract18Mar2020-24Mar2020.csv',
                '207JourneyDataExtract25Mar2020-31Mar2020.csv',
                '208JourneyDataExtract01Apr2020-07Apr2020.csv',
                '209JourneyDataExtract08Apr2020-14Apr2020.csv',
                '20JourneyDataExtract24Aug2016-30Aug2016.csv',
                '210JourneyDataExtract15Apr2020-21Apr2020.csv',
                '211JourneyDataExtract22Apr2020-28Apr2020.csv',
                '212JourneyDataExtract29Apr2020-05May2020.csv',
                '213JourneyDataExtract06May2020-12May2020.csv',
                '214JourneyDataExtract13May2020-19May2020.csv',
                '215JourneyDataExtract20May2020-26May2020.csv',
                '216JourneyDataExtract27May2020-02Jun2020.csv',
                '217JourneyDataExtract03Jun2020-09Jun2020.csv',
                '218JourneyDataExtract10Jun2020-16Jun2020.csv',
                '219JourneyDataExtract17Jun2020-23Jun2020.csv',
                '21JourneyDataExtract31Aug2016-06Sep2016.csv',
                '220JourneyDataExtract24Jun2020-30Jun2020.csv',
                '221JourneyDataExtract01Jul2020-07Jul2020.csv',
                '222JourneyDataExtract08Jul2020-14Jul2020.csv',
                '223JourneyDataExtract15Jul2020-21Jul2020.csv',
                '224JourneyDataExtract22Jul2020-28Jul2020.csv',
                '225JourneyDataExtract29Jul2020-04Aug2020.csv',
                '226JourneyDataExtract05Aug2020-11Aug2020.csv',
                '227JourneyDataExtract12Aug2020-18Aug2020.csv',
                '228JourneyDataExtract19Aug2020-25Aug2020.csv',
                '229JourneyDataExtract26Aug2020-01Sep2020.csv',
                '22JourneyDataExtract07Sep2016-13Sep2016.csv',
                '230JourneyDataExtract02Sep2020-08Sep2020.csv',
                '231JourneyDataExtract09Sep2020-15Sep2020.csv',
                '232JourneyDataExtract16Sep2020-22Sep2020.csv',
                '233JourneyDataExtract23Sep2020-29Sep2020.csv',
                '234JourneyDataExtract30Sep2020-06Oct2020.csv',
                '235JourneyDataExtract07Oct2020-13Oct2020.csv',
                '236JourneyDataExtract14Oct2020-20Oct2020.csv',
                '237JourneyDataExtract21Oct2020-27Oct2020.csv',
                '238JourneyDataExtract28Oct2020-03Nov2020.csv',
                '239JourneyDataExtract04Nov2020-10Nov2020.csv',
                '23JourneyDataExtract14Sep2016-20Sep2016.csv',
                '240JourneyDataExtract11Nov2020-17Nov2020.csv',
                '241JourneyDataExtract18Nov2020-24Nov2020.csv',
                '242JourneyDataExtract25Nov2020-01Dec2020.csv',
                '243JourneyDataExtract02Dec2020-08Dec2020.csv',
                '244JourneyDataExtract09Dec2020-15Dec2020.csv',
                '245JourneyDataExtract16Dec2020-22Dec2020.csv',
                '246JourneyDataExtract23Dec2020-29Dec2020.csv',
                '246JourneyDataExtract30Dec2020-05Jan2021.csv',
                '247JourneyDataExtract06Jan2021-12Jan2021.csv',
                '248JourneyDataExtract13Jan2021-19Jan2021.csv',
                '249JourneyDataExtract20Jan2021-26Jan2021.csv',
                '24JourneyDataExtract21Sep2016-27Sep2016.csv',
                '250JourneyDataExtract27Jan2021-02Feb2021.csv',
                '251JourneyDataExtract03Feb2021-09Feb2021.csv',
                '252JourneyDataExtract10Feb2021-16Feb2021.csv',
                '253JourneyDataExtract17Feb2021-23Feb2021.csv',
                '254JourneyDataExtract24Feb2021-02Mar2021.csv',
                '255JourneyDataExtract03Mar2021-09Mar2021.csv',
                '256JourneyDataExtract10Mar2021-16Mar2021.csv',
                '257JourneyDataExtract17Mar2021-23Mar2021.csv',
                '258JourneyDataExtract24Mar2021-30Mar2021.csv',
                '259JourneyDataExtract31Mar2021-06Apr2021.csv',
                '25JourneyDataExtract28Sep2016-04Oct2016.csv',
                '260JourneyDataExtract07Apr2021-13Apr2021.csv',
                '261JourneyDataExtract14Apr2021-20Apr2021.csv',
                '262JourneyDataExtract21Apr2021-27Apr2021.csv',
                '263JourneyDataExtract28Apr2021-04May2021.csv',
                '264JourneyDataExtract05May2021-11May2021.csv',
                '265JourneyDataExtract12May2021-18May2021.csv',
                '266JourneyDataExtract19May2021-25May2021.csv',
                '267JourneyDataExtract26May2021-01Jun2021.csv',
                '268JourneyDataExtract02Jun2021-08Jun2021.csv',
                '269JourneyDataExtract09Jun2021-15Jun2021.csv',
                '26JourneyDataExtract05Oct2016-11Oct2016.csv',
                '270JourneyDataExtract16Jun2021-22Jun2021.csv',
                '271JourneyDataExtract23Jun2021-29Jun2021.csv',
                '272JourneyDataExtract30Jun2021-06Jul2021.csv',
                '273JourneyDataExtract07Jul2021-13Jul2021.csv',
                '274JourneyDataExtract14Jul2021-20Jul2021.csv',
                '275JourneyDataExtract21Jul2021-27Jul2021.csv',
                '276JourneyDataExtract28Jul2021-03Aug2021.csv',
                '277JourneyDataExtract04Aug2021-10Aug2021.csv',
                '278JourneyDataExtract11Aug2021-17Aug2021.csv',
                '279JourneyDataExtract18Aug2021-24Aug2021.csv',
                '27JourneyDataExtract12Oct2016-18Oct2016.csv',
                '280JourneyDataExtract25Aug2021-31Aug2021.csv',
                '281JourneyDataExtract01Sep2021-07Sep2021.csv',
                '282JourneyDataExtract08Sep2021-14Sep2021.csv',
                '283JourneyDataExtract15Sep2021-21Sep2021.csv',
                '284JourneyDataExtract22Sep2021-28Sep2021.csv',
                '285JourneyDataExtract29Sep2021-05Oct2021.csv',
                '286JourneyDataExtract06Oct2021-12Oct2021.csv',
                '287JourneyDataExtract13Oct2021-19Oct2021.csv',
                '288JourneyDataExtract20Oct2021-26Oct2021.csv',
                '289JourneyDataExtract27Oct2021-02Nov2021.csv',
                '28JourneyDataExtract19Oct2016-25Oct2016.csv',
                '290JourneyDataExtract03Nov2021-09Nov2021.csv',
                '291JourneyDataExtract10Nov2021-16Nov2021.csv',
                '292JourneyDataExtract17Nov2021-23Nov2021.csv',
                '293JourneyDataExtract24Nov2021-30Nov2021.csv',
                '294JourneyDataExtract01Dec2021-07Dec2021.csv',
                '295JourneyDataExtract08Dec2021-14Dec2021.csv',
                '296JourneyDataExtract15Dec2021-21Dec2021.csv',
                '297JourneyDataExtract22Dec2021-28Dec2021.csv',
                '298JourneyDataExtract29Dec2021-04Jan2022.csv',
                '299JourneyDataExtract05Jan2022-11Jan2022.csv',
                '29JourneyDataExtract26Oct2016-01Nov2016.csv',
                '2a.JourneyDataExtract01Feb15-14Feb15.csv',
                '2b.JourneyDataExtract15Feb15-28Feb15.csv',
                '300JourneyDataExtract12Jan2022-18Jan2022.csv',
                '301JourneyDataExtract19Jan2022-25Jan2022.csv',
                '302JourneyDataExtract26Jan2022-01Feb2022.csv',
                '303JourneyDataExtract02Feb2022-08Feb2022.csv',
                '304JourneyDataExtract09Feb2022-15Feb2022.csv',
                '305JourneyDataExtract16Feb2022-22Feb2022.csv',
                '306JourneyDataExtract23Feb2022-01Mar2022.csv',
                '307JourneyDataExtract02Mar2022-08Mar2022.csv',
                '308JourneyDataExtract09Mar2022-15Mar2022.csv',
                '309JourneyDataExtract16Mar2022-22Mar2022.csv',
                '30JourneyDataExtract02Nov2016-08Nov2016.csv',
                '310JourneyDataExtract23Mar2022-29Mar2022.csv',
                '311JourneyDataExtract30Mar2022-05Apr2022.csv',
                '312JourneyDataExtract06Apr2022-12Apr2022.csv',
                '313JourneyDataExtract13Apr2022-19Apr2022.csv',
                '314JourneyDataExtract20Apr2022-26Apr2022.csv',
                '315JourneyDataExtract27Apr2022-03May2022.csv',
                '316JourneyDataExtract04May2022-10May2022.csv',
                '317JourneyDataExtract11May2022-17May2022.csv',
                '318JourneyDataExtract18May2022-24May2022.csv',
                '319JourneyDataExtract25May2022-31May2022.csv',
                '31JourneyDataExtract09Nov2016-15Nov2016.csv',
                '320JourneyDataExtract01Jun2022-07Jun2022.csv',
                '321JourneyDataExtract08Jun2022-14Jun2022.csv',
                '322JourneyDataExtract15Jun2022-21Jun2022.csv',
                '323JourneyDataExtract22Jun2022-28Jun2022.csv',
                '324JourneyDataExtract29Jun2022-05Jul2022.csv',
                '325JourneyDataExtract06Jul2022-12Jul2022.csv',
                '326JourneyDataExtract13Jul2022-19Jul2022.csv',
                '327JourneyDataExtract20Jul2022-26Jul2022.csv',
                '328JourneyDataExtract27Jul2022-02Aug2022.csv',
                '329JourneyDataExtract03Aug2022-09Aug2022.csv',
                '32JourneyDataExtract16Nov2016-22Nov2016.csv',
                '330JourneyDataExtract10Aug2022-16Aug2022.csv',
                '331JourneyDataExtract17Aug2022-23Aug2022.csv',
                '332JourneyDataExtract24Aug2022-30Aug2022.csv',
                '333JourneyDataExtract31Aug2022-06Sep2022.csv',
                '334JourneyDataExtract07Sep2022-11Sep2022.csv',
                '335JourneyDataExtract12Sep2022-18Sep2022.csv',
                '336JourneyDataExtract19Sep2022-25Sep2022.csv',
                '337JourneyDataExtract26Sep2022-02Oct2022.csv',
                '338JourneyDataExtract03Oct2022-09Oct2022.csv',
                '339JourneyDataExtract10Oct2022-16Oct2022.csv',
                '33JourneyDataExtract23Nov2016-29Nov2016.csv',
                '340JourneyDataExtract17Oct2022-23Oct2022.csv',
                '341JourneyDataExtract24Oct2022-30Oct2022.csv',
                '342JourneyDataExtract31Oct2022-06Nov2022.csv',
                '343JourneyDataExtract07Nov2022-13Nov2022.csv',
                '344JourneyDataExtract14Nov2022-20Nov2022.csv',
                '345JourneyDataExtract21Nov2022-27Nov2022.csv',
                '346JourneyDataExtract28Nov2022-04Dec2022.csv',
                '347JourneyDataExtract05Dec2022-11Dec2022.csv',
                '348JourneyDataExtract12Dec2022-18Dec2022.csv',
                '349JourneyDataExtract19Dec2022-25Dec2022.csv',
                '34JourneyDataExtract30Nov2016-06Dec2016.csv',
                '350JourneyDataExtract26Dec2022-01Jan2023.csv',
                '351JourneyDataExtract02Jan2023-08Jan2023.csv',
                '352JourneyDataExtract09Jan2023-15Jan2023.csv',
                '353JourneyDataExtract16Jan2023-22Jan2023.csv',
                '354JourneyDataExtract23Jan2023-29Jan2023.csv',
                '355JourneyDataExtract30Jan2023-05Feb2023.csv',
                '356JourneyDataExtract06Feb2023-12Feb2023.csv',
                '357JourneyDataExtract13Feb2023-19Feb2023.csv',
                '358JourneyDataExtract20Feb2023-26Feb2023.csv',
                '359JourneyDataExtract27Feb2023-05Mar2023.csv',
                '35JourneyDataExtract07Dec2016-13Dec2016.csv',
                '360JourneyDataExtract06Mar2023-12Mar2023.csv',
                '361JourneyDataExtract13Mar2023-19Mar2023.csv',
                '362JourneyDataExtract20Mar2023-26Mar2023.csv',
                '363JourneyDataExtract27Mar2023-02Apr2023.csv',
                '364JourneyDataExtract03Apr2023-09Apr2023.csv',
                '365JourneyDataExtract10Apr2023-16Apr2023.csv',
                '366JourneyDataExtract17Apr2023-23Apr2023.csv',
                '367JourneyDataExtract24Apr2023-30Apr2023.csv',
                '368JourneyDataExtract01May2023-07May2023.csv',
                '369JourneyDataExtract08May2023-14May2023.csv',
                '36JourneyDataExtract14Dec2016-20Dec2016.csv',
                '370JourneyDataExtract15May2023-21May2023.csv',
                '371JourneyDataExtract22May2023-28May2023.csv',
                '372JourneyDataExtract29May2023-04Jun2023.csv',
                '373JourneyDataExtract05Jun2023-11Jun2023.csv',
                '374JourneyDataExtract12Jun2023-18Jun2023.csv',
                '375JourneyDataExtract19Jun2023-30Jun2023.csv',
                '376JourneyDataExtract01Jul2023-14Jul2023.csv',
                '377JourneyDataExtract15Jul2023-31Jul2023.csv',
                '378JourneyDataExtract01Aug2023-14Aug2023.csv',
                '378JourneyDataExtract15Aug2023-31Aug2023.csv',
                '379JourneyDataExtract01Sep2023-14Sep2023.csv',
                '37JourneyDataExtract21Dec2016-27Dec2016.csv',
                '380JourneyDataExtract15Sep2023-30Sep2023.csv',
                '381JourneyDataExtract01Oct2023-14Oct2023.csv',
                '382JourneyDataExtract15Oct2023-31Oct2023.csv',
                '383JourneyDataExtract01Nov2023-14Nov2023.csv',
                '384JourneyDataExtract15Nov2023-30Nov2023.csv',
                '385JourneyDataExtract01Dec2023-14Dec2023.csv',
                '386JourneyDataExtract15Dec2023-31Dec2023.csv',
                '387JourneyDataExtract01Jan2024-14Jan2024.csv',
                '388JourneyDataExtract15Jan2024-31Jan2024.csv',
                '389JourneyDataExtract01Feb2024-14Feb2024.csv',
                '38JourneyDataExtract28Dec2016-03Jan2017.csv',
                '390JourneyDataExtract15Feb2024-29Feb2024.csv',
                '391JourneyDataExtract01Mar2024-14Mar2024.csv',
                '392JourneyDataExtract15Mar2024-31Mar2024.csv',
                '393JourneyDataExtract01Apr2024-14Apr2024.csv',
                '394JourneyDataExtract15Apr2024-30Apr2024.csv',
                '39JourneyDataExtract04Jan2017-10Jan2017.csv',
                '3a.JourneyDataExtract01Mar15-15Mar15.csv',
                '3b.JourneyDataExtract16Mar15-31Mar15.csv',
                '40JourneyDataExtract11Jan2017-17Jan2017.csv',
                '41JourneyDataExtract18Jan2017-24Jan2017.csv',
                '42JourneyDataExtract25Jan2017-31Jan2017.csv',
                '43JourneyDataExtract01Feb2017-07Feb2017.csv',
                '44JourneyDataExtract08Feb2017-14Feb2017.csv',
                '45JourneyDataExtract15Feb2017-21Feb2017.csv',
                '46JourneyDataExtract22Feb2017-28Feb2017.csv',
                '47JourneyDataExtract01Mar2017-07Mar2017.csv',
                '48JourneyDataExtract08Mar2017-14Mar2017.csv',
                '4a.JourneyDataExtract01Apr15-16Apr15.csv',
                '4b.JourneyDataExtract%2017Apr15-02May15.csv',
                '50%20Journey%20Data%20Extract%2022Mar2017-28Mar2017.csv',
                '51%20Journey%20Data%20Extract%2029Mar2017-04Apr2017.csv',
                '52%20Journey%20Data%20Extract%2005Apr2017-11Apr2017.csv',
                '53JourneyDataExtract12Apr2017-18Apr2017.csv',
                '54JourneyDataExtract19Apr2017-25Apr2017.csv',
                '55JourneyData%20Extract26Apr2017-02May2017.csv',
                '56JourneyDataExtract%2003May2017-09May2017.csv',
                '57JourneyDataExtract10May2017-16May2017.csv',
                '58JourneyDataExtract17May2017-23May2017.csv',
                '59JourneyDataExtract24May2017-30May2017.csv',
                '5a.JourneyDataExtract03May15-16May15.csv',
                '5b.JourneyDataExtract17May15-30May15.csv',
                '60JourneyDataExtract31May2017-06Jun2017.csv',
                '61JourneyDataExtract07Jun2017-13Jun2017.csv',
                '62JourneyDataExtract14Jun2017-20Jun2017.csv',
                '63JourneyDataExtract21Jun2017-27Jun2017.csv',
                '64JourneyDataExtract28Jun2017-04Jul2017.csv',
                '65JourneyDataExtract05Jul2017-11Jul2017.csv',
                '66JourneyDataExtract12Jul2017-18Jul2017.csv',
                '67JourneyDataExtract19Jul2017-25Jul2017.csv',
                '68JourneyDataExtract26Jul2017-31Jul2017.csv',
                '69JourneyDataExtract01Aug2017-07Aug2017.csv',
                '6aJourneyDataExtract31May15-12Jun15.csv',
                '6bJourneyDataExtract13Jun15-27Jun15.csv',
                '70JourneyDataExtract08Aug2017-14Aug2017.csv',
                '71JourneyDataExtract15Aug2017-22Aug2017.csv',
                '72JourneyDataExtract23Aug2017-29Aug2017.csv',
                '73JourneyDataExtract30Aug2017-05Sep2017.csv',
                '74JourneyDataExtract06Sep2017-12Sep2017.csv',
                '75JourneyDataExtract13Sep2017-19Sep2017.csv',
                '76JourneyDataExtract20Sep2017-26Sep2017.csv',
                '77JourneyDataExtract27Sep2017-03Oct2017.csv',
                '78JourneyDataExtract04Oct2017-10Oct2017.csv',
                '79JourneyDataExtract11Oct2017-17Oct2017.csv',
                '7a.JourneyDataExtract28Jun15-11Jul15.csv',
                '7b.JourneyDataExtract12Jul15-25Jul15.csv',
                '80JourneyDataExtract18Oct2017-24Oct2017.csv',
                '81JourneyDataExtract25Oct2017-31Oct2017.csv',
                '82JourneyDataExtract01Nov2017-07Nov2017.csv',
                '83JourneyDataExtract08Nov2017-14Nov2017.csv',
                '84JourneyDataExtract15Nov2017-21Nov2017.csv',
                '85JourneyDataExtract22Nov2017-28Nov2017.csv',
                '86JourneyDataExtract29Nov2017-05Dec2017.csv',
                '87JourneyDataExtract06Dec2017-12Dec2017.csv',
                '88JourneyDataExtract13Dec2017-19Dec2017.csv',
                '89JourneyDataExtract20Dec2017-26Dec2017.csv',
                '8a-Journey-Data-Extract-26Jul15-07Aug15.csv',
                '8b-Journey-Data-Extract-08Aug15-22Aug15.csv',
                '90JourneyDataExtract27Dec2017-02Jan2018.csv',
                '91JourneyDataExtract03Jan2018-09Jan2018.csv',
                '92JourneyDataExtract10Jan2018-16Jan2018.csv',
                '93JourneyDataExtract17Jan2018-23Jan2018.csv',
                '94JourneyDataExtract24Jan2018-30Jan2018.csv',
                '95JourneyDataExtract31Jan2018-06Feb2018.csv',
                '96JourneyDataExtract07Feb2018-13Feb2018.csv',
                '97JourneyDataExtract14Feb2018-20Feb2018.csv',
                '98JourneyDataExtract21Feb2018-27Feb2018.csv',
                '99JourneyDataExtract28Feb2018-06Mar2018.csv',
                '9a-Journey-Data-Extract-23Aug15-05Sep15.csv',
                '9b-Journey-Data-Extract-06Sep15-19Sep15.csv']

file_names_attempt_2 = ['350JourneyDataExtract26Dec2022-01Jan2023.csv',
                '351JourneyDataExtract02Jan2023-08Jan2023.csv',
                '352JourneyDataExtract09Jan2023-15Jan2023.csv',
                '353JourneyDataExtract16Jan2023-22Jan2023.csv',
                '354JourneyDataExtract23Jan2023-29Jan2023.csv',
                '355JourneyDataExtract30Jan2023-05Feb2023.csv',
                '356JourneyDataExtract06Feb2023-12Feb2023.csv',
                '357JourneyDataExtract13Feb2023-19Feb2023.csv',
                '358JourneyDataExtract20Feb2023-26Feb2023.csv',
                '359JourneyDataExtract27Feb2023-05Mar2023.csv',
                '35JourneyDataExtract07Dec2016-13Dec2016.csv',
                '360JourneyDataExtract06Mar2023-12Mar2023.csv',
                '361JourneyDataExtract13Mar2023-19Mar2023.csv',
                '362JourneyDataExtract20Mar2023-26Mar2023.csv',
                '363JourneyDataExtract27Mar2023-02Apr2023.csv',
                '364JourneyDataExtract03Apr2023-09Apr2023.csv',
                '365JourneyDataExtract10Apr2023-16Apr2023.csv',
                '366JourneyDataExtract17Apr2023-23Apr2023.csv',
                '367JourneyDataExtract24Apr2023-30Apr2023.csv',
                '368JourneyDataExtract01May2023-07May2023.csv',
                '369JourneyDataExtract08May2023-14May2023.csv',
                '36JourneyDataExtract14Dec2016-20Dec2016.csv',
                '370JourneyDataExtract15May2023-21May2023.csv',
                '371JourneyDataExtract22May2023-28May2023.csv',
                '372JourneyDataExtract29May2023-04Jun2023.csv',
                '373JourneyDataExtract05Jun2023-11Jun2023.csv',
                '374JourneyDataExtract12Jun2023-18Jun2023.csv',
                '375JourneyDataExtract19Jun2023-30Jun2023.csv',
                '376JourneyDataExtract01Jul2023-14Jul2023.csv',
                '377JourneyDataExtract15Jul2023-31Jul2023.csv',
                '378JourneyDataExtract01Aug2023-14Aug2023.csv',
                '378JourneyDataExtract15Aug2023-31Aug2023.csv',
                '379JourneyDataExtract01Sep2023-14Sep2023.csv',
                '37JourneyDataExtract21Dec2016-27Dec2016.csv',
                '380JourneyDataExtract15Sep2023-30Sep2023.csv',
                '381JourneyDataExtract01Oct2023-14Oct2023.csv',
                '382JourneyDataExtract15Oct2023-31Oct2023.csv',
                '383JourneyDataExtract01Nov2023-14Nov2023.csv',
                '384JourneyDataExtract15Nov2023-30Nov2023.csv',
                '385JourneyDataExtract01Dec2023-14Dec2023.csv',
                '386JourneyDataExtract15Dec2023-31Dec2023.csv',
                '387JourneyDataExtract01Jan2024-14Jan2024.csv',
                '388JourneyDataExtract15Jan2024-31Jan2024.csv',
                '389JourneyDataExtract01Feb2024-14Feb2024.csv',
                '38JourneyDataExtract28Dec2016-03Jan2017.csv',
                '390JourneyDataExtract15Feb2024-29Feb2024.csv',
                '391JourneyDataExtract01Mar2024-14Mar2024.csv',
                '392JourneyDataExtract15Mar2024-31Mar2024.csv',
                '393JourneyDataExtract01Apr2024-14Apr2024.csv',
                '394JourneyDataExtract15Apr2024-30Apr2024.csv',
                '39JourneyDataExtract04Jan2017-10Jan2017.csv',
                '3a.JourneyDataExtract01Mar15-15Mar15.csv',
                '3b.JourneyDataExtract16Mar15-31Mar15.csv',
                '40JourneyDataExtract11Jan2017-17Jan2017.csv',
                '41JourneyDataExtract18Jan2017-24Jan2017.csv',
                '42JourneyDataExtract25Jan2017-31Jan2017.csv',
                '43JourneyDataExtract01Feb2017-07Feb2017.csv',
                '44JourneyDataExtract08Feb2017-14Feb2017.csv',
                '45JourneyDataExtract15Feb2017-21Feb2017.csv',
                '46JourneyDataExtract22Feb2017-28Feb2017.csv',
                '47JourneyDataExtract01Mar2017-07Mar2017.csv',
                '48JourneyDataExtract08Mar2017-14Mar2017.csv',
                '4a.JourneyDataExtract01Apr15-16Apr15.csv',
                '4b.JourneyDataExtract%2017Apr15-02May15.csv',
                '50%20Journey%20Data%20Extract%2022Mar2017-28Mar2017.csv',
                '51%20Journey%20Data%20Extract%2029Mar2017-04Apr2017.csv',
                '52%20Journey%20Data%20Extract%2005Apr2017-11Apr2017.csv',
                '53JourneyDataExtract12Apr2017-18Apr2017.csv',
                '54JourneyDataExtract19Apr2017-25Apr2017.csv',
                '55JourneyData%20Extract26Apr2017-02May2017.csv',
                '56JourneyDataExtract%2003May2017-09May2017.csv',
                '57JourneyDataExtract10May2017-16May2017.csv',
                '58JourneyDataExtract17May2017-23May2017.csv',
                '59JourneyDataExtract24May2017-30May2017.csv',
                '5a.JourneyDataExtract03May15-16May15.csv',
                '5b.JourneyDataExtract17May15-30May15.csv',
                '60JourneyDataExtract31May2017-06Jun2017.csv',
                '61JourneyDataExtract07Jun2017-13Jun2017.csv',
                '62JourneyDataExtract14Jun2017-20Jun2017.csv',
                '63JourneyDataExtract21Jun2017-27Jun2017.csv',
                '64JourneyDataExtract28Jun2017-04Jul2017.csv',
                '65JourneyDataExtract05Jul2017-11Jul2017.csv',
                '66JourneyDataExtract12Jul2017-18Jul2017.csv',
                '67JourneyDataExtract19Jul2017-25Jul2017.csv',
                '68JourneyDataExtract26Jul2017-31Jul2017.csv',
                '69JourneyDataExtract01Aug2017-07Aug2017.csv',
                '6aJourneyDataExtract31May15-12Jun15.csv',
                '6bJourneyDataExtract13Jun15-27Jun15.csv',
                '70JourneyDataExtract08Aug2017-14Aug2017.csv',
                '71JourneyDataExtract15Aug2017-22Aug2017.csv',
                '72JourneyDataExtract23Aug2017-29Aug2017.csv',
                '73JourneyDataExtract30Aug2017-05Sep2017.csv',
                '74JourneyDataExtract06Sep2017-12Sep2017.csv',
                '75JourneyDataExtract13Sep2017-19Sep2017.csv',
                '76JourneyDataExtract20Sep2017-26Sep2017.csv',
                '77JourneyDataExtract27Sep2017-03Oct2017.csv',
                '78JourneyDataExtract04Oct2017-10Oct2017.csv',
                '79JourneyDataExtract11Oct2017-17Oct2017.csv',
                '7a.JourneyDataExtract28Jun15-11Jul15.csv',
                '7b.JourneyDataExtract12Jul15-25Jul15.csv',
                '80JourneyDataExtract18Oct2017-24Oct2017.csv',
                '81JourneyDataExtract25Oct2017-31Oct2017.csv',
                '82JourneyDataExtract01Nov2017-07Nov2017.csv',
                '83JourneyDataExtract08Nov2017-14Nov2017.csv',
                '84JourneyDataExtract15Nov2017-21Nov2017.csv',
                '85JourneyDataExtract22Nov2017-28Nov2017.csv',
                '86JourneyDataExtract29Nov2017-05Dec2017.csv',
                '87JourneyDataExtract06Dec2017-12Dec2017.csv',
                '88JourneyDataExtract13Dec2017-19Dec2017.csv',
                '89JourneyDataExtract20Dec2017-26Dec2017.csv',
                '8a-Journey-Data-Extract-26Jul15-07Aug15.csv',
                '8b-Journey-Data-Extract-08Aug15-22Aug15.csv',
                '90JourneyDataExtract27Dec2017-02Jan2018.csv',
                '91JourneyDataExtract03Jan2018-09Jan2018.csv',
                '92JourneyDataExtract10Jan2018-16Jan2018.csv',
                '93JourneyDataExtract17Jan2018-23Jan2018.csv',
                '94JourneyDataExtract24Jan2018-30Jan2018.csv',
                '95JourneyDataExtract31Jan2018-06Feb2018.csv',
                '96JourneyDataExtract07Feb2018-13Feb2018.csv',
                '97JourneyDataExtract14Feb2018-20Feb2018.csv',
                '98JourneyDataExtract21Feb2018-27Feb2018.csv',
                '99JourneyDataExtract28Feb2018-06Mar2018.csv',
                '9a-Journey-Data-Extract-23Aug15-05Sep15.csv',
                '9b-Journey-Data-Extract-06Sep15-19Sep15.csv']

s3 = boto3.client('s3')
s3_bucket_name = 'tfl-cycle-data'

# Directory to save downloaded CSV files
download_dir = 'temp/'

# Download each CSV file
for file_name in file_names_attempt_2:
    s3_file_key = f'JourneyInfo/{file_name.replace("%20", "_")}'
    file_url = base_url + file_name
    response = requests.get(file_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Save the CSV file
        file_path = os.path.join(download_dir, file_name.replace("%20", "_"))
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {file_name}")
        
        s3.upload_file(file_path, s3_bucket_name, s3_file_key)
        print("Uploaded to S3")
        os.remove(file_path)
        print("Deleted local file")
    else:
        print(f"Failed to download {file_name}, Status code: {response.status_code}")

print("All files downloaded.")
