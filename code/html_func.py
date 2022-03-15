import os
from git import Repo


def make_html_eng():
    "Create html with figures embedded"

    print("Making html file in english...")
    html_figs_div = [
        "cases_hosp_deaths_eng_div.html",
        "deaths_eng_div.html",
        "hospitalizations_per_severity_eng_div.html",
        "hospitalizations_per_vacc_per_100_000_eng_div.html",
        "hospitalizations_per_vacc_per_100_000_ratio_eng_div.html",
        "hospitalizations_per_vaccination_eng_div.html",
        "vaccinations_by_age_eng_div.html",
    ]

    div_dict = {}
    for div_html in html_figs_div:
        with open(os.path.join("../plots/", div_html), "r") as f:
            div_dict[div_html.split(".")[0]] = f.read()

    html_str = f"""
    <!DOCTYPE html>
    <html>

    <head>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" href="code/css/style.css">
        <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-3QS9XM17RH"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());

            gtag('config', 'G-3QS9XM17RH');
        </script>

    </head>

    <body class="container">
        <h1>Covid-19 & Vaccination numbers in Cyprus </h1>        
        <p>Produced by <i>Georgios Michail</i> (<a href="https://orcid.org/0000-0001-7018-937X" target="_blank">ORCID</a>\
            , <a href="https://www.linkedin.com/in/gm032/" target="_blank">LinkedIn</a>)</p>

        <p>Website exists also in &nbsp<a href="https://geomich.github.io/covid_cyprus/covid_cy_report_gr.html" target="_blank"">
            <img src="greece.png" alt="Greek" style="width:26px;height:26px;">
        </a>
        </p

        <p>This set of graphs on the situation of the COVID-19 pandemic in Cyprus is produced & updated based on data from the ministry of health.</p>

        <p> <i>Sources from Cyprus Μinistry of Ηealth</i>: \
            <a href="https://www.data.gov.cy/dataset/%CE%B7%CE%BC%CE%B5%CF%81%CE%AE%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B1%CF%84%CE%B9%CF%83%CF%84%CE%B9%CE%BA%CE%AC-%CE%B4%CE%B9%CE%B1%CF%83%CF%80%CE%BF%CF%81%CE%AC%CF%82-%CF%84%CE%B7%CF%82-%CE%BD%CF%8C%CF%83%CE%BF%CF%85-covid-19-%CF%83%CF%84%CE%B7%CE%BD-%CE%BA%CF%8D%CF%80%CF%81%CE%BF"\
                target="_blank">dataset 1</a>, \
            <a href="https://www.data.gov.cy/dataset/%CE%B5%CE%B2%CE%B4%CE%BF%CE%BC%CE%B1%CE%B4%CE%B9%CE%B1%CE%AF%CE%B1-%CF%83%CF%84%CE%B1%CF%84%CE%B9%CF%83%CF%84%CE%B9%CE%BA%CE%AC-%CE%B5%CE%BC%CE%B2%CE%BF%CE%BB%CE%B9%CE%B1%CF%83%CE%BC%CF%8E%CE%BD-%CE%BA%CE%B1%CF%84%CE%AC-%CF%84%CE%B7%CF%82-%CE%BD%CF%8C%CF%83%CE%BF%CF%85-covid-19-%CE%B1%CE%BD%CE%AC-%CE%BF%CE%BC%CE%AC%CE%B4%CE%B1-%CF%83%CF%84%CF%8C%CF%87%CE%BF"\
                target="_blank">dataset 2</a>, \
            <a href="https://www.pio.gov.cy/coronavirus/categories/press#30"
                target="_blank">daily reports</a></p> 

        <p>The figures are interactive and you can zoom in to get higher resolution, or hover over some points to get extra information.</p>
        <h3>Daily new cases, hospitalizations & deaths</h3>

        <p>The first two figures show the time course of the positive cases, hospitalizations and deaths associated with COVID-19.</p>
        <br>

        {div_dict["cases_hosp_deaths_eng_div"]}
        <br><br>

        {div_dict["deaths_eng_div"]}
        <br>

        <h3>Daily new hospitalizations by vaccination status</h3>
        
        <br>

        <p>The next graph shows the hospitalizations related to COVID-19 by vaccination status. Here, one can easily notice that the possibility \
            to be hospitalized after an infection is quite larger for unvaccinated people. </p>
        <br>

        {div_dict["hospitalizations_per_vaccination_eng_div"]}
        <br>

        <h3>But how much more likely is to be hospitalized after an infection if unvaccinated vs. vaccinated?</h3>
        <br>

        <p>Some people based on figures similar to the previous one say that, if on one day we have 80 hospitalizations of \
            unvaccinated and 20 of vaccinated people, this means it's 4 times more likely to be hospitalized for unvaccinated.\
            This is actually not accurate, because when doing this calculation we don't take into account the overall size\
            of vaccinated and unvaccinated sub-populations from which these hospitalizations come from. \
            To be correct, we need to compare hospitalizations for the same number of vaccinated and unvaccinated people.\
            This is what I show in the following figure, depicting hospitalizations per 100 000 vaccinated and 100 000 unvaccinated people. \
            And here it becomes clear that the chances of being hospitalized if unvaccinated are from 5 up \
            to approx. 20 times higher than when vaccinated. </p>
        <br>

        {div_dict["hospitalizations_per_vacc_per_100_000_eng_div"]}
        <br>
        
        <p>And here you see the ratio between hospitalizations in 100 000 unvaccinated and 100 000 vaccinated people, \
            which corresponds to how many times more likely is to be hospitalized if unvaccinated vs. \
            vaccinated. Vaccination reduces markedly the likelihood of being hospitalized. </p>
        <br>

        {div_dict["hospitalizations_per_vacc_per_100_000_ratio_eng_div"]}
        <br>

        <h3>And what about the severity of hospitalizations?</h3>
        <br>
        <p>This figure splits hospitalizations in 3 categories:</p>
         <ol>
            <li>Patients not being treated in an Intensive Care Unit (ICU).</li>
            <li>Patients in ICU but not intubated.</li>
            <li>Patients in ICU, intubated and supported with mechanical ventilation.</li>
        </ol>
        <p>The line "Severe" in the graph refers to the number of cases assessed as severe in the total amount of hospitalised patients, \
            independent of beloning to any of the above categories. This metric is useful because there are cases\
            that are severe even if they are not treated in an ICU.</p>
        <br>

        {div_dict["hospitalizations_per_severity_eng_div"]}
        <br>

        <h3>Immunity wall of Cyprus</h3>
        <br>

        <p>What is the vaccination level for the different age groups? </p>
        <br>

        {div_dict["vaccinations_by_age_eng_div"]}

    </body>

    </html>
    """

    # The final string can be saved in a file
    print("Saving html file...")
    with open("../covid_cy_report.html", "w") as f:
        f.write(html_str)


def make_html_gr():
    "Create html with embedded graphs in greek"

    print("Making html file in greek...")
    html_figs_div = [
        "cases_hosp_deaths_gr_div.html",
        "deaths_gr_div.html",
        "hospitalizations_per_severity_gr_div.html",
        "hospitalizations_per_vacc_per_100_000_gr_div.html",
        "hospitalizations_per_vacc_per_100_000_ratio_gr_div.html",
        "hospitalizations_per_vaccination_gr_div.html",
        "vaccinations_by_age_gr_div.html",
    ]

    div_dict = {}
    for div_html in html_figs_div:
        with open(os.path.join("../plots/", div_html), "r") as f:
            div_dict[div_html.split(".")[0]] = f.read()

    html_str = f"""
    <!DOCTYPE html>
    <html>

    <head>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" href="code/css/style.css">
        <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-GTZQ5CCC2Y"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());

            gtag('config', 'G-GTZQ5CCC2Y');
        </script>

    </head>

    <body class="container">
        <h1>Στατιστική εικόνα πανδημίας COVID-19 και εμβολιασμών στην Κύπρο</h1>
        <p>Δημιουργήθηκε από τον <i>Γιώργο Μιχαήλ</i> (<a href="https://orcid.org/0000-0001-7018-937X" target="_blank">ORCID</a>\
            , <a href="https://www.linkedin.com/in/gm032/" target="_blank">LinkedIn</a>)</p>
        
        <p>Η ιστοσελίδα υπάρχει και στα &nbsp<a href="https://geomich.github.io/covid_cyprus/covid_cy_report.html" target="_blank"">
            <img src="united-kingdom.png" alt="English" style="width:26px;height:26px;">
        </a>
        </p

        <p>Αυτές οι γραφικές παραστάσεις για την πανδημική κατάσταση στην Κύπρο βασίζονται σε δεδομένα του Υπ. Υγείας.</p>

        <p> <i>Πηγές</i>: \
            <a href="https://www.data.gov.cy/dataset/%CE%B7%CE%BC%CE%B5%CF%81%CE%AE%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B1%CF%84%CE%B9%CF%83%CF%84%CE%B9%CE%BA%CE%AC-%CE%B4%CE%B9%CE%B1%CF%83%CF%80%CE%BF%CF%81%CE%AC%CF%82-%CF%84%CE%B7%CF%82-%CE%BD%CF%8C%CF%83%CE%BF%CF%85-covid-19-%CF%83%CF%84%CE%B7%CE%BD-%CE%BA%CF%8D%CF%80%CF%81%CE%BF"\
                target="_blank">dataset 1</a>, \
            <a href="https://www.data.gov.cy/dataset/%CE%B5%CE%B2%CE%B4%CE%BF%CE%BC%CE%B1%CE%B4%CE%B9%CE%B1%CE%AF%CE%B1-%CF%83%CF%84%CE%B1%CF%84%CE%B9%CF%83%CF%84%CE%B9%CE%BA%CE%AC-%CE%B5%CE%BC%CE%B2%CE%BF%CE%BB%CE%B9%CE%B1%CF%83%CE%BC%CF%8E%CE%BD-%CE%BA%CE%B1%CF%84%CE%AC-%CF%84%CE%B7%CF%82-%CE%BD%CF%8C%CF%83%CE%BF%CF%85-covid-19-%CE%B1%CE%BD%CE%AC-%CE%BF%CE%BC%CE%AC%CE%B4%CE%B1-%CF%83%CF%84%CF%8C%CF%87%CE%BF"\
                target="_blank">dataset 2</a>, \
            <a href="https://www.pio.gov.cy/coronavirus/categories/press#30"
                target="_blank">καθημερινές αναφορές</a></p> 

        <p>Οι παρακάτω γραφικές είναι διαδραστικές και μπορείς να κάνεις ζουμ για μεγαλύτερη ακρίβεια ή περισσότερες λεπτομέρειες. 
        <h3>Ημερήσια κρούσματα, νοσηλείες και θάνατοι </h3>
        <br>

        {div_dict["cases_hosp_deaths_gr_div"]}
        <br><br>

        {div_dict["deaths_gr_div"]}
        <br>

        <h3>Ημερήσιες νοσηλείες ανά εμβολιαστικό στάτους</h3>
        
        <br>

        {div_dict["hospitalizations_per_vaccination_gr_div"]}
        <br>

        <h3>Ποια είναι όμως η ακριβής διαφορά στην πιθανότητα νοσηλείας για έναν ανεμβολίαστο συγκριτικά με έναν εμβολιασμένο </h3>
        <br>

        <p>Με βάση την παραπάνω γρ. παράσταση, αν μια μέρα έχουμε 80 νοσηλείες ανεμβολίαστων και 20 εμβολιασμένων, μια γρήγορη σκέψη \
            είναι ότι οι ανεμβολίαστοι έχουν 4 φορές μεγαλύτερη πιθανότητα νοσηλείας. Αυτό όμως δεν είναι ακριβές, γιατί δεν λαμβάνει υπόψη 
            το μέγεθος των υπό-πληθυσμών ανεμβολιάστων και εμβολιασμένων από τους οποίους προέρχονται αυτές οι νοσηλέιες. Για να είμαστε ακρίβείς \
            πρέπει να συγκρίνουμε νοσηλείες σε ίσο πληθυσμό εμβολιασμένων και ανεμβολίαστων. Αυτό είναι που κάνει η παρακάτω γραφική παράσταση, η οποία \
            αναπαριστά τον εβδομαδιαίο μέσο όρο νοσηλειών ανά 100 000 εμβολιασμένους και 100 000 ανεμβολίαστους. Με βάση αυτή τη γραφική παράσταση,\
            η πιθανότητα νοσηλείας για έναν ανεμβολίαστο είναι από 5 μέχρι σχεδόν 20 φορές μεγαλύτερη συγκριτικά με έναν εμβολιασμένο. <p>
        <br>

        {div_dict["hospitalizations_per_vacc_per_100_000_gr_div"]}
        <br>
        
        <p>Η παρακάτω γραφική παράσταση δείχνει την αναλογία νοσηλείων σε πληθυσμό 100 000 ανεμβολιάστων προς 100 000 εμβολιασμένων. \
            Αυτή η αναλογία αντιστοιχεί με το πόσες φορές πιο πιθανό είναι να νοσηλευτεί ένας ανεμβολίαστος συγκριτικά με ένα εμβολιασμένο. </p>
        <br>

        {div_dict["hospitalizations_per_vacc_per_100_000_ratio_gr_div"]}
        <br>

        <h3>Σοβαρότητα νοσηλειών</h3>
        <br>
        <p>Σε αυτή τη γραφική οι νοσηλείες διαχωρίζονται σε 3 κατηγορίες:</p>
         <ol>
            <li>Ασθενείς που δεν νοσηλεύονται στην εντατική.</li>
            <li>Ασθενείς που νοσηλεύονται στην εντατική αλλά δεν έχουν διασωληνωθεί.</li>
            <li>Ασθενείς που νοσηλεύονται στην εντατική και έχουν διασωληνωθεί.</li>
        </ol>
        <p>Η γραμμή "Σοβαρά" στη γραφική παράσταση αντιστοιχεί στις νοσηλείες που κρίνοται ως σοβαρές ανεξάρτητα με την παραπάνω κατηγοριοποίηση.\
            Αυτό το στοιχείο είναι χρήσιμο γιατί υπάρχουν νοσηλείες που είναι σε σοβαρή κατάσταση έστω κι αν ο ασθενής δεν είναι στην εντατική.</p>
        <br>

        {div_dict["hospitalizations_per_severity_gr_div"]}
        <br>

        <h3>Εμβολιαστική κάλυψη στην Κύπρο</h3>
        <br>

        {div_dict["vaccinations_by_age_gr_div"]}

    </body>

    </html>
    """

    # The final string can be saved in a file
    print("Saving html file...")
    with open("../covid_cy_report_gr.html", "w") as f:
        f.write(html_str)


def make_html_gr_bootstrap():

    "Create html with embedded graphs in greek"
    print("Making html file in greek...")
    html_figs_div = [
        "cases_hosp_deaths_gr_div.html",
        "deaths_gr_div.html",
        "hospitalizations_per_severity_gr_div.html",
        "hospitalizations_per_vacc_per_100_000_gr_div.html",
        "hospitalizations_per_vacc_per_100_000_ratio_gr_div.html",
        "hospitalizations_per_vaccination_gr_div.html",
        "vaccinations_by_age_gr_div.html",
    ]

    div_dict = {}
    for div_html in html_figs_div:
        with open(os.path.join("../plots/", div_html), "r") as f:
            div_dict[div_html.split(".")[0]] = f.read()

    html_str = f"""
    <!DOCTYPE html>
    <html>

    <head>
        <link rel="stylesheet" type="text/css" href="code/css/style_v1.css">
        <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>

    </head>
    <body">
    <div class="container">
        <div class="container p-4 my-4 bg-dark text-white">

        <h1>Στατιστική εικόνα πανδημίας COVID-19 και εμβολιασμών στην Κύπρο</h1>
        <p class="text-secondary" >Δημιουργήθηκε από τον <i>Γιώργο Μιχαήλ</i> (<a href="https://orcid.org/0000-0001-7018-937X" target="_blank">ORCID</a>\
            , <a href="https://www.linkedin.com/in/gm032/" target="_blank">LinkedIn</a>)</p>
        <p class="text-secondary" >Η ιστοσελίδα υπάρχει και στα&nbsp<a href="https://geomich.github.io/covid_cyprus/covid_cy_report.html" style="text-decoration:none" target="_blank"">
            <img src="united-kingdom.png" alt="English" style="width:20px;height:20px;">
        </a>
        </p>
        </div>

        <div class="container p-4 my-4 border">

        <p>Αυτές οι γραφικές παραστάσεις για την πανδημική κατάσταση στην Κύπρο βασίζονται σε δεδομένα του Υπ. Υγείας.</p>

        <p> <i>Πηγές</i>: \
            <a href="https://www.data.gov.cy/dataset/%CE%B7%CE%BC%CE%B5%CF%81%CE%AE%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B1%CF%84%CE%B9%CF%83%CF%84%CE%B9%CE%BA%CE%AC-%CE%B4%CE%B9%CE%B1%CF%83%CF%80%CE%BF%CF%81%CE%AC%CF%82-%CF%84%CE%B7%CF%82-%CE%BD%CF%8C%CF%83%CE%BF%CF%85-covid-19-%CF%83%CF%84%CE%B7%CE%BD-%CE%BA%CF%8D%CF%80%CF%81%CE%BF"\
                target="_blank">dataset 1</a>, \
            <a href="https://www.data.gov.cy/dataset/%CE%B5%CE%B2%CE%B4%CE%BF%CE%BC%CE%B1%CE%B4%CE%B9%CE%B1%CE%AF%CE%B1-%CF%83%CF%84%CE%B1%CF%84%CE%B9%CF%83%CF%84%CE%B9%CE%BA%CE%AC-%CE%B5%CE%BC%CE%B2%CE%BF%CE%BB%CE%B9%CE%B1%CF%83%CE%BC%CF%8E%CE%BD-%CE%BA%CE%B1%CF%84%CE%AC-%CF%84%CE%B7%CF%82-%CE%BD%CF%8C%CF%83%CE%BF%CF%85-covid-19-%CE%B1%CE%BD%CE%AC-%CE%BF%CE%BC%CE%AC%CE%B4%CE%B1-%CF%83%CF%84%CF%8C%CF%87%CE%BF"\
                target="_blank">dataset 2</a>, \
            <a href="https://www.pio.gov.cy/coronavirus/categories/press#30"
                target="_blank">καθημερινές αναφορές</a></p> 

        <p>Οι παρακάτω γραφικές είναι διαδραστικές και μπορείς να κάνεις ζουμ για μεγαλύτερη ακρίβεια ή περισσότερες λεπτομέρειες. 

        <table class="table table-bordered table-sm">
            <thead>
                <tr class="table-primary">
                    <th>Ημερομηνία</th>
                    <th>Κρούσματα</th>
                    <th>Nοσηλείες (% ανεμβολίαστων)</th>
                    <th>Θάνατοι</th>
                </tr>
            </thead>
            <tbody>   
                <tr class="table-primary">
                    <td>16 Ιανουαρίου</td>
                    <td>1971</td>
                    <td>270 (71.4%)</td>
                    <td>6</td>
                </tr>
            </tbody>
        </table>

        <h3>Ημερήσια κρούσματα, νοσηλείες και θάνατοι </h3>
        <br>

        {div_dict["cases_hosp_deaths_gr_div"]}

        <br><br>

        {div_dict["deaths_gr_div"]}
        <br>

        <h3>Ημερήσιες νοσηλείες ανά εμβολιαστικό στάτους</h3>
        
        <br>

        {div_dict["hospitalizations_per_vaccination_gr_div"]}
        <br>

        <h3>Ποια είναι όμως η ακριβής διαφορά στην πιθανότητα νοσηλείας για έναν ανεμβολίαστο συγκριτικά με έναν εμβολιασμένο </h3>
        <br>

        <p>Με βάση την παραπάνω γρ. παράσταση, αν μια μέρα έχουμε 80 νοσηλείες ανεμβολίαστων και 20 εμβολιασμένων, μια γρήγορη σκέψη \
            είναι ότι οι ανεμβολίαστοι έχουν 4 φορές μεγαλύτερη πιθανότητα νοσηλείας. Αυτό όμως δεν είναι ακριβές, γιατί δεν λαμβάνει υπόψη 
            το μέγεθος των υπό-πληθυσμών ανεμβολιάστων και εμβολιασμένων από τους οποίους προέρχονται αυτές οι νοσηλέιες. Για να είμαστε ακρίβείς \
            πρέπει να συγκρίνουμε νοσηλείες σε ίσο πληθυσμό εμβολιασμένων και ανεμβολίαστων. Αυτό είναι που κάνει η παρακάτω γραφική παράσταση, η οποία \
            αναπαριστά τον εβδομαδιαίο μέσο όρο νοσηλειών ανά 100 000 εμβολιασμένους και 100 000 ανεμβολίαστους. Με βάση αυτή τη γραφική παράσταση,\
            η πιθανότητα νοσηλείας για έναν ανεμβολίαστο είναι από 5 μέχρι σχεδόν 20 φορές μεγαλύτερη συγκριτικά με έναν εμβολιασμένο. <p>
        <br>

        {div_dict["hospitalizations_per_vacc_per_100_000_gr_div"]}
        <br>
        
        <p>Η παρακάτω γραφική παράσταση δείχνει την αναλογία νοσηλείων σε πληθυσμό 100 000 ανεμβολιάστων προς 100 000 εμβολιασμένων. \
            Αυτή η αναλογία αντιστοιχεί με το πόσες φορές πιο πιθανό είναι να νοσηλευτεί ένας ανεμβολίαστος συγκριτικά με ένα εμβολιασμένο. </p>
        <br>

        {div_dict["hospitalizations_per_vacc_per_100_000_ratio_gr_div"]}
        <br>

        <h3>Σοβαρότητα νοσηλειών</h3>
        <br>
        <p>Σε αυτή τη γραφική οι νοσηλείες διαχωρίζονται σε 3 κατηγορίες:</p>
         <ol>
            <li>Ασθενείς που δεν νοσηλεύονται στην εντατική.</li>
            <li>Ασθενείς που νοσηλεύονται στην εντατική αλλά δεν έχουν διασωληνωθεί.</li>
            <li>Ασθενείς που νοσηλεύονται στην εντατική και έχουν διασωληνωθεί.</li>
        </ol>
        <p>Η γραμμή "Σοβαρά" στη γραφική παράσταση αντιστοιχεί στις νοσηλείες που κρίνοται ως σοβαρές ανεξάρτητα με την παραπάνω κατηγοριοποίηση.\
            Αυτό το στοιχείο είναι χρήσιμο γιατί υπάρχουν νοσηλείες που είναι σε σοβαρή κατάσταση έστω κι αν ο ασθενής δεν είναι στην εντατική.</p>
        <br>

        {div_dict["hospitalizations_per_severity_gr_div"]}
        <br>

        <h3>Εμβολιαστική κάλυψη στην Κύπρο</h3>
        <br>

        {div_dict["vaccinations_by_age_gr_div"]}
        </div>
    </div>
    </body>

    </html>
    """

    # The final string can be saved in a file
    print("Saving html file...")
    with open("../covid_cy_report_gr_bootstrap.html", "w") as f:
        f.write(html_str)


def git_push_new_html():
    "pushing to remote"
    print("Git pushing html..")
    PATH_OF_GIT_REPO = r"/home/geomi/gm/projects/playground/covid_cy/.git"  # make sure .git folder is properly configured
    COMMIT_MESSAGE = "updating html file"
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add("covid_cy_report.html", update=True)
        repo.git.add("covid_cy_report_gr.html", update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name="origin")
        origin.push()
    except:
        print("Some error occured while pushing the code")
