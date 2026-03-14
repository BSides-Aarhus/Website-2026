/**
 * Cookie Consent configuration for BSides Aarhus 2026
 * Library: orestbida/cookieconsent v3 (self-hosted)
 * Compliance: GDPR + ePrivacy Directive (Denmark/EU)
 *
 * Privacy-first: All tracking scripts are blocked by default.
 * Nothing loads until you explicitly opt in.
 */

var lang = document.documentElement.lang || 'en';

CookieConsent.run({
  guiOptions: {
    consentModal: {
      layout: 'box inline',
      position: 'bottom left'
    },
    preferencesModal: {
      layout: 'box'
    }
  },

  categories: {
    necessary: {
      enabled: true,
      readOnly: true
    },
    analytics: {
      autoClear: {
        cookies: [
          { name: /^_ga/ },
          { name: '_gid' }
        ]
      }
    },
    marketing: {
      autoClear: {
        cookies: [
          { name: /^li_/ },
          { name: 'lidc' },
          { name: 'bcookie' },
          { name: 'UserMatchHistory' },
          { name: 'AnalyticsSyncHistory' },
          { name: 'ln_or' }
        ]
      }
    }
  },

  onConsent: function () {
    if (CookieConsent.acceptedCategory('analytics')) {
      gtag('consent', 'update', {
        'analytics_storage': 'granted'
      });
    }
    if (CookieConsent.acceptedCategory('marketing')) {
      gtag('consent', 'update', {
        'ad_storage': 'granted',
        'ad_user_data': 'granted',
        'ad_personalization': 'granted'
      });
    }
  },

  onChange: function () {
    gtag('consent', 'update', {
      'analytics_storage': CookieConsent.acceptedCategory('analytics') ? 'granted' : 'denied',
      'ad_storage': CookieConsent.acceptedCategory('marketing') ? 'granted' : 'denied',
      'ad_user_data': CookieConsent.acceptedCategory('marketing') ? 'granted' : 'denied',
      'ad_personalization': CookieConsent.acceptedCategory('marketing') ? 'granted' : 'denied'
    });
  },

  language: {
    default: lang === 'da' ? 'da' : 'en',
    translations: {
      en: {
        consentModal: {
          title: 'We block all tracking by default',
          description: 'As a security conference, we practice what we preach. All analytics and marketing scripts are <strong>disabled by default</strong> — nothing tracks you unless you explicitly opt in. If you\'d like to help us improve the site, you can enable analytics below. <a href="/privacy/">Privacy Policy</a>',
          acceptAllBtn: 'Accept all',
          acceptNecessaryBtn: 'Reject all',
          showPreferencesBtn: 'Manage preferences'
        },
        preferencesModal: {
          title: 'Cookie Preferences',
          acceptAllBtn: 'Accept all',
          acceptNecessaryBtn: 'Reject all',
          savePreferencesBtn: 'Save preferences',
          sections: [
            {
              title: 'Your Privacy First',
              description: 'BSides Aarhus is a security and privacy community. We block all non-essential scripts by default. No tracking fires until you say so. Using a privacy browser like Brave or Firefox with tracking protection? We respect that — the site works fully without any cookies.'
            },
            {
              title: 'Strictly Necessary',
              description: 'Essential for the website to function: Cloudflare security cookies and your consent preference. Cannot be disabled.',
              linkedCategory: 'necessary'
            },
            {
              title: 'Analytics (disabled by default)',
              description: 'Google Analytics helps us understand visitor patterns — which talks generate interest, where traffic comes from. This data helps us plan a better conference. Only enabled if you opt in.',
              linkedCategory: 'analytics',
              cookieTable: {
                headers: { name: 'Name', domain: 'Domain', description: 'Description', expiration: 'Expiration' },
                body: [
                  { name: '_ga', domain: 'bsidesaarhus.dk', description: 'Distinguishes unique visitors', expiration: '2 years' },
                  { name: '_gid', domain: 'bsidesaarhus.dk', description: 'Distinguishes unique visitors', expiration: '24 hours' }
                ]
              }
            },
            {
              title: 'Marketing (disabled by default)',
              description: 'LinkedIn Insight Tag helps us measure how well our LinkedIn posts drive conference awareness. Only enabled if you opt in.',
              linkedCategory: 'marketing',
              cookieTable: {
                headers: { name: 'Name', domain: 'Domain', description: 'Description', expiration: 'Expiration' },
                body: [
                  { name: 'li_sugr', domain: '.linkedin.com', description: 'Browser identifier', expiration: '3 months' },
                  { name: 'UserMatchHistory', domain: '.linkedin.com', description: 'Ad delivery synchronization', expiration: '30 days' }
                ]
              }
            },
            {
              title: 'More Information',
              description: 'Questions? Contact <a href="mailto:info@bsidesaarhus.dk">info@bsidesaarhus.dk</a>. Read our full <a href="/privacy/">Privacy Policy</a>.'
            }
          ]
        }
      },
      da: {
        consentModal: {
          title: 'Vi blokerer al sporing som standard',
          description: 'Som sikkerhedskonference praktiserer vi, hvad vi pr\u00e6diker. Alle analyse- og markedsf\u00f8ringsscripts er <strong>deaktiveret som standard</strong> — intet sporer dig, medmindre du eksplicit v\u00e6lger det. Vil du hj\u00e6lpe os med at forbedre siden, kan du aktivere analyse herunder. <a href="/da/privacy/">Privatlivspolitik</a>',
          acceptAllBtn: 'Accepter alle',
          acceptNecessaryBtn: 'Afvis alle',
          showPreferencesBtn: 'Administrer pr\u00e6ferencer'
        },
        preferencesModal: {
          title: 'Cookie-pr\u00e6ferencer',
          acceptAllBtn: 'Accepter alle',
          acceptNecessaryBtn: 'Afvis alle',
          savePreferencesBtn: 'Gem pr\u00e6ferencer',
          sections: [
            {
              title: 'Dit Privatliv F\u00f8rst',
              description: 'BSides Aarhus er et sikkerheds- og privatlivsf\u00e6llesskab. Vi blokerer alle ikke-essentielle scripts som standard. Ingen sporing aktiveres, f\u00f8r du siger ja. Bruger du en privatlivsbrowser som Brave eller Firefox med sporingsbeskyttelse? Vi respekterer det — siden fungerer fuldt uden cookies.'
            },
            {
              title: 'Strengt N\u00f8dvendige',
              description: 'Essentielle for at hjemmesiden kan fungere: Cloudflare-sikkerhedscookies og din samtykkepræference. Kan ikke deaktiveres.',
              linkedCategory: 'necessary'
            },
            {
              title: 'Analyse (deaktiveret som standard)',
              description: 'Google Analytics hj\u00e6lper os med at forst\u00e5 bes\u00f8gsm\u00f8nstre — hvilke foredrag der skaber interesse, hvor trafikken kommer fra. Disse data hj\u00e6lper os med at planl\u00e6gge en bedre konference. Aktiveres kun, hvis du v\u00e6lger det.',
              linkedCategory: 'analytics',
              cookieTable: {
                headers: { name: 'Navn', domain: 'Dom\u00e6ne', description: 'Beskrivelse', expiration: 'Udl\u00f8b' },
                body: [
                  { name: '_ga', domain: 'bsidesaarhus.dk', description: 'Skelner unikke bes\u00f8gende', expiration: '2 \u00e5r' },
                  { name: '_gid', domain: 'bsidesaarhus.dk', description: 'Skelner unikke bes\u00f8gende', expiration: '24 timer' }
                ]
              }
            },
            {
              title: 'Markedsf\u00f8ring (deaktiveret som standard)',
              description: 'LinkedIn Insight Tag hj\u00e6lper os med at m\u00e5le, hvor godt vores LinkedIn-opslag skaber opm\u00e6rksomhed om konferencen. Aktiveres kun, hvis du v\u00e6lger det.',
              linkedCategory: 'marketing',
              cookieTable: {
                headers: { name: 'Navn', domain: 'Dom\u00e6ne', description: 'Beskrivelse', expiration: 'Udl\u00f8b' },
                body: [
                  { name: 'li_sugr', domain: '.linkedin.com', description: 'Browseridentifikator', expiration: '3 m\u00e5neder' },
                  { name: 'UserMatchHistory', domain: '.linkedin.com', description: 'Annonceleveringssynkronisering', expiration: '30 dage' }
                ]
              }
            },
            {
              title: 'Mere Information',
              description: 'Sp\u00f8rgsm\u00e5l? Kontakt <a href="mailto:info@bsidesaarhus.dk">info@bsidesaarhus.dk</a>. L\u00e6s vores fulde <a href="/da/privacy/">Privatlivspolitik</a>.'
            }
          ]
        }
      }
    }
  }
});
