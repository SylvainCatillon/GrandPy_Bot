import pytest
import requests

from app.utils import api_getter as script


class MockMapsResponse:
    """Mock the response of Google Maps API"""
    @staticmethod
    def json():
        """Mock the .json() method of
        a response object returned by requests.get()"""
        return {
            "candidates": [{
                "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                "geometry": {
                    "location": {
                        "lat": 48.8748465,
                        "lng": 2.3504873
                    },
                    "viewport": {
                        "northeast": {
                            "lat": 48.87622362989272,
                            "lng": 2.351843679892722
                        },
                        "southwest": {
                            "lat": 48.87352397010727,
                            "lng": 2.349144020107278
                        }
                    }
                },
                "name": "OpenClassrooms"
            }],
            "status": "OK"
        }

class MockWikiGeoloc:
    """Mock the response of Wikipedia Geoloc API"""
    @staticmethod
    def json():
        """Mock the .json() method of
        a response object returned by requests.get()"""
        return {
            "query": {
                "geosearch": [{
                    "pageid": 5091748,
                    "ns": 0,
                    "title": "H\u00f4tel Bourrienne",
                    "lat": 48.874525,
                    "lon": 2.3511388888889,
                    "dist": 59.6,
                    "primary": ""
                }]
            }
        }

class MockWikiParse:
    """Mock the response of Wikipedia Parse API"""
    @staticmethod
    def json():
        """Mock the .json() method of
        a response object returned by requests.get()"""
        return {
            "parse": {
                "title": "Hôtel Bourrienne",
                "pageid": 5091748,
                "text": "<div class=\"mw-parser-output\"><h2><span class=\"mw-headline\" id=\"Histoire\">Histoire</span><span class=\"mw-editsection\"><span class=\"mw-editsection-bracket\">[</span><a href=\"/w/index.php?title=H%C3%B4tel_Bourrienne&amp;veaction=edit&amp;section=1\" class=\"mw-editsection-visualeditor\" title=\"Modifier la section : Histoire\">modifier</a><span class=\"mw-editsection-divider\"> | </span><a href=\"/w/index.php?title=H%C3%B4tel_Bourrienne&amp;action=edit&amp;section=1\" title=\"Modifier la section : Histoire\">modifier le code</a><span class=\"mw-editsection-bracket\">]</span></span></h2>\n<p>Justine Segard<sup id=\"cite_ref-1\" class=\"reference\"><a href=\"#cite_note-1\"><span class=\"cite_crochet\">[</span>1<span class=\"cite_crochet\">]</span></a></sup>, femme de Préponnier de Bazin et dame de Dampierre, entreprend la construction de l'hôtel en 1787, laquelle s'achève en 1793, à l'époque où le quartier du <a href=\"/wiki/Faubourg_Poissonni%C3%A8re\" title=\"Faubourg Poissonnière\">Faubourg Poissonnière</a> s'urbanise. \n</p><p>L'hôtel, alors qu'il n'est pas encore terminé, passe entre plusieurs mains et arrive en 1792 dans celle des époux Lormier-Lagrave dont la fille Fortunée épouse peu après Antoine Hamelin, fournisseur général des armées. Les parents en font don à la fille, qui le fit sans doute décorer par <a href=\"/wiki/Fran%C3%A7ois-Joseph_B%C3%A9langer\" title=\"François-Joseph Bélanger\">François-Joseph Bélanger</a><sup id=\"cite_ref-2\" class=\"reference\"><a href=\"#cite_note-2\"><span class=\"cite_crochet\">[</span>2<span class=\"cite_crochet\">]</span></a></sup>. <a href=\"/wiki/Fortun%C3%A9e_Hamelin\" title=\"Fortunée Hamelin\">Fortunée Hamelin</a> devient une personnalité en vue du <a href=\"/wiki/Directoire_(R%C3%A9volution)\" class=\"mw-redirect\" title=\"Directoire (Révolution)\">Directoire</a> et du <a href=\"/wiki/Consulat_(histoire_de_France)\" title=\"Consulat (histoire de France)\">Consulat</a>, tenant à l'hôtel un salon renommé sous le nom de la <i><a href=\"/wiki/Incroyables_et_Merveilleuses\" title=\"Incroyables et Merveilleuses\">Merveilleuse</a></i> Madame Hamelin. Native de Saint-Domingue, elle était amie avec <a href=\"/wiki/Jos%C3%A9phine_de_Beauharnais\" title=\"Joséphine de Beauharnais\">Joséphine de Beauharnais</a>.\n</p><p>En 1798, l'hôtel est vendu à Louis Prévost qui le revend 100&#160;000 francs à <a href=\"/wiki/Louis_Antoine_Fauvelet_de_Bourrienne\" title=\"Louis Antoine Fauvelet de Bourrienne\">Louis Antoine Fauvelet de Bourrienne</a>, secrétaire particulier et ami de <a href=\"/wiki/Napol%C3%A9on_Bonaparte\" class=\"mw-redirect\" title=\"Napoléon Bonaparte\">Napoléon Bonaparte</a>, qui lui donna son nom et y fit faire d'importantes transformations par l'architecte <a href=\"/wiki/%C3%89tienne-Ch%C3%A9rubin_Leconte\" title=\"Étienne-Chérubin Leconte\">Étienne-Chérubin Leconte</a>. Subissant les aléas de la politique, Bourrienne réussit cependant une brillante carrière sous la <a href=\"/wiki/Seconde_Restauration\" title=\"Seconde Restauration\">Restauration</a> et jusqu'en 1824, les salons de l'hôtel furent parmi les plus brillants de Paris, animés par sa femme. Mais la <a href=\"/wiki/Trois_Glorieuses\" title=\"Trois Glorieuses\">Révolution de 1830</a> lui fait perdre sa fortune. Entre-temps, l'hôtel avait été vendu à plusieurs reprises. En 1826, <a href=\"/wiki/Henri_Duponchel\" title=\"Henri Duponchel\">Henri Duponchel</a> travaille sur le décor néo-pompéien de l'hôtel<sup id=\"cite_ref-3\" class=\"reference\"><a href=\"#cite_note-3\"><span class=\"cite_crochet\">[</span>3<span class=\"cite_crochet\">]</span></a></sup>.\n</p><p>\nCharles Tuleu acquiert l'hôtel à Lucien Charles Alexandre de Berny en 1886 qui dirige une fonderie de caractères d'imprimerie. Charles Tuleu prend la direction de la fonderie en gardant la même raison sociale et installe ses ateliers dans le jardin<sup id=\"cite_ref-4\" class=\"reference\"><a href=\"#cite_note-4\"><span class=\"cite_crochet\">[</span>4<span class=\"cite_crochet\">]</span></a></sup>. L'hôtel est resté dans la famille jusqu'en 2015.</p><div class=\"mw-references-wrap\"><ol class=\"references\">\n<li id=\"cite_note-1\"><span class=\"mw-cite-backlink noprint\"><a href=\"#cite_ref-1\">↑</a> </span><span class=\"reference-text\">D'après <a href=\"/wiki/Jacques_Hillairet\" title=\"Jacques Hillairet\">Jacques Hillairet</a>, <i>Dictionnaire historique des rues de Paris</i>, éd. de Minuit, 1963.</span>\n</li>\n<li id=\"cite_note-2\"><span class=\"mw-cite-backlink noprint\"><a href=\"#cite_ref-2\">↑</a> </span><span class=\"reference-text\">Claude Frégnac, <i>Belles demeures de Paris</i>, Hachette, 1977,  <small style=\"line-height:1em;\">(<a href=\"/wiki/International_Standard_Book_Number\" title=\"International Standard Book Number\">ISBN</a>&#160;<a href=\"/wiki/Sp%C3%A9cial:Ouvrages_de_r%C3%A9f%C3%A9rence/9782010038686\" title=\"Spécial:Ouvrages de référence/9782010038686\"><span class=\"nowrap\">9782010038686</span></a>)</small>, <span class=\"nowrap\"><abbr class=\"abbr\" title=\"page\">p.</abbr>&#160;261</span>.</span>\n</li>\n<li id=\"cite_note-3\"><span class=\"mw-cite-backlink noprint\"><a href=\"#cite_ref-3\">↑</a> </span><span class=\"reference-text\">Anne Dion-Tenenbaum, <i><a rel=\"nofollow\" class=\"external text\" href=\"http://www.persee.fr/web/revues/home/prescript/article/rvart_0035-1326_1997_num_116_1_348329\">Multiple Duponchel</a></i>, Revue de l'Art, 1997, <abbr class=\"abbr\" title=\"numéro\">n<sup>o</sup></abbr>&#160;116, <span class=\"nowrap\"><abbr class=\"abbr\" title=\"page(s)\">p.</abbr>&#160;66-67</span>.</span>\n</li>\n<li id=\"cite_note-4\"><span class=\"mw-cite-backlink noprint\"><a href=\"#cite_ref-4\">↑</a> </span><span class=\"reference-text\"><span class=\"ouvrage\"><a rel=\"nofollow\" class=\"external text\" href=\"http://data.bnf.fr/14938494/charles_tuleu/\">«&#160;<cite style=\"font-style: normal;\">Charles Tuleu (1851-1934) - Auteur - Ressources de la Bibliothèque nationale de France</cite>&#160;»</a>, sur <span class=\"italique\">data.bnf.fr</span> <small style=\"line-height:1em;\">(consulté le <span class=\"nowrap\">10 décembre 2017</span>)</small></span></span>\n</li>\n</ol></div>\n<!-- \nNewPP limit report\nParsed by mw1233\nCached time: 20200214103824\nCache expiry: 2592000\nDynamic content: false\nComplications: []\nCPU time usage: 0.148 seconds\nReal time usage: 0.197 seconds\nPreprocessor visited node count: 175/1000000\nPost‐expand include size: 1605/2097152 bytes\nTemplate argument size: 66/2097152 bytes\nHighest expansion depth: 12/40\nExpensive parser function count: 0/500\nUnstrip recursion depth: 0/20\nUnstrip post‐expand size: 844/5000000 bytes\nNumber of Wikibase entities loaded: 0/400\nLua time usage: 0.072/10.000 seconds\nLua memory usage: 1.91 MB/50 MB\n-->\n<!--\nTransclusion expansion time report (%,ms,calls,template)\n100.00%  142.117      1 -total\n 43.11%   61.270      1 Modèle:ISBN\n 41.17%   58.504      1 Modèle:Lien_web\n 10.82%   15.375      2 Modèle:P.\n  8.11%   11.529      2 Modèle:Abréviation_discrète\n  5.25%    7.466      2 Modèle:Est_nombre_entier\n  4.47%    6.348      1 Modèle:N°\n  2.16%    3.075      2 Modèle:Trim\n-->\n</div>"}}

@pytest.fixture
def mock_response(monkeypatch):
    """Requests.get() mocked."""

    def mock_get(*args, **kwargs):
        """Returns a Mock object, accorded to the request"""
        for arg in args:
            if "googleapis" in arg:
                return MockMapsResponse()
            if "wikipedia" in arg and "params" in kwargs:
                params = kwargs["params"]
                if "action" in params:
                    if params["action"] == "query":
                        return MockWikiGeoloc()
                    if params["action"] == "parse":
                        return MockWikiParse()


    monkeypatch.setattr(requests, "get", mock_get)

class TestApiGetter:
    """Test the class ApiGetter"""
    def setup_method(self):
        """Prepare the tests by creating an instance of ApiGetter"""
        self.api_getter = script.ApiGetter()

    def test_get_maps_response(self, mock_response):
        """Assures that ApiGetter.request_address get
        a response from Google Maps API"""
        result = self.api_getter.request_address("fake query")
        assert result == MockMapsResponse.json()

    def test_get_address(self, mock_response):
        """Assures that the mocked address is in
        the dict returned by ApiGetter.get_address()"""
        result = self.api_getter.main(["fake", "querry"])
        assert "7 Cité Paradis, 75010 Paris, France" in result["address"]

    def test_get_story(self, mock_response):
        """Assures that the mocked story is in
        the dict returned by ApiGetter.get_address()"""
        result = self.api_getter.main(["fake", "querry"])
        assert "Justine Segard" in result["story"]

    def test_main(self, mock_response):
        """Assures that the dict returned by ApiGetter.get_address()
        contains the required keys"""
        result = self.api_getter.main(["fake", "querry"])
        for key in ["status", "address", "map_url", "story"]:
            assert key in result
        assert result["status"] == "OK"

    def test_address_not_found(self):
        """Tests ApiGetter.main() with  a query which isn't an address"""
        result = self.api_getter.main(["qwertyuiopasdfghjklm"])
        assert result["status"] == "ADDRESS_NOT_FOUND"
