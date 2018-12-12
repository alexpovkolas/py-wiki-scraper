from scraper import spider


def do():
    starter = ["/wiki/Main_Page", "/wiki/Wikipedia", "/wiki/Free_content", "/wiki/Encyclopedia",
               "/wiki/English_language", "/wiki/Benjamin_Tillman",
               "/wiki/Democratic_Party_(United_States)", "/wiki/Governor_of_South_Carolina",
               "/wiki/United_States_Senate", "/wiki/White_supremacist",
               "/wiki/African_Americans", "/wiki/Red_Shirts_(United_States)",
               "/wiki/South_Carolina_gubernatorial_election,_1876"]
    spider(starter, 10000)


do()
