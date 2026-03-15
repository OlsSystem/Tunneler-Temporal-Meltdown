# ---- Python Modules ---- #
import pygame
from modules.utils.TextButton import TextButton
from modules.utils.TextLabel import TextLabel
from modules.menus.menuUtils import buildChapterButtons, buildLevelButtons, fetchTime

class LeaderboardMenu:
    def __init__(self, screen, handTracking, cursor, levelGenerator, clock, rootDir, tunneler, InputHandler, MenuHandler, brightnessHandler, dataHandler):
        self.enabled = False
        self.screen = screen
        self.HT = handTracking
        self.LG = levelGenerator
        self.cursor = cursor
        self.rootDir = rootDir
        self.clock = clock
        self.tunneler = tunneler
        self.InputHandler = InputHandler
        self.MenuHandler = MenuHandler
        self.brightnessSurface = brightnessHandler
        self.db = dataHandler
        
        # initialises the ui
        self.fetchAllUsers = self.db.fetchAllUsers

        self.chapterId = None
        self.levelId = None

        self.title = TextLabel(736, 50, "Leaderboard", 64, (255, 255, 255), screen)
        self.backButton = TextButton(736, 796, "Back", 36, (200, 50, 50), screen)

        self.scoreLabels = []
        self.chapterButtons = []
        self.levelButtons = []

        # builds the chapter buttons
        buildChapterButtons(self)

    def enableUi(self):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def buildLeaderboard(self):
        self.scoreLabels.clear()

        users = list(self.fetchAllUsers())
        levelKey = f"{self.chapterId}/{self.levelId}"

        entries = []

        # loops through all the users for fetching the time for the current level key set
        for user in users:
            username = user.get("username")
            levelTimes = user.get("levelTimes", {})

            if levelKey in levelTimes:
                entries.append({
                    "username": username,
                    "timeString": levelTimes[levelKey],
                    "timeSeconds": fetchTime(self, levelTimes[levelKey]) # converts the XX:XX:XX to seconds
                })

        # uses a lambda function to sort the times into decending order
        entries.sort(key=lambda x: x["timeSeconds"])

        # loops through all entries and appends them to an array
        y = 200
        for i, entry in enumerate(entries): # uses enumeration to get the index of each entry
            label = TextLabel(
                736,
                y,
                f"{i + 1}. {entry['username']} - {entry['timeString']}",
                36,
                (255, 255, 255),
                self.screen
            )
            self.scoreLabels.append(label)
            y += 60

        if not entries:
            self.scoreLabels.append(
                TextLabel(736, 200, "No scores yet!", 36, (255, 255, 255), self.screen)
            )

    def drawCurrentMenu(self):
        if not self.enabled:
            return

        self.title.draw()
        self.backButton.draw()

        # draws on items based on where its at. 
        if self.chapterId is None:
            for chapterId, button in self.chapterButtons:
                button.draw()

        elif self.levelId is None:
            for chapterId, levelId, button in self.levelButtons:
                button.draw()
        else: # draws on the scores 
            for label in self.scoreLabels:
                label.draw()

        for event in pygame.event.get():
            self.InputHandler.inputCheck(event)

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.backButton.isClicked(event.pos):
                    if self.levelId is not None:
                        self.levelId = None
                    elif self.chapterId is not None:
                        self.chapterId = None
                    else:
                        self.MenuHandler.enablePreviousMenu()
                    return

                # builds level buttons if the chapter is selected
                if self.chapterId is None:
                    for chapterId, button in self.chapterButtons:
                        if button.isClicked(event.pos):
                            self.chapterId = chapterId
                            buildLevelButtons(self, chapterId)
                            return

                # builds the leaderboard if the level and chapter are selected     
                if self.levelId is None:
                    for chapterId, levelId, button in self.levelButtons:
                        if button.isClicked(event.pos):
                            self.levelId = levelId
                            self.buildLeaderboard()
                            return