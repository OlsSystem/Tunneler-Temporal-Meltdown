# ---- Python Modules ---- #
import pygame
from modules.utils.TextButton import TextButton
from modules.utils.TextLabel import TextLabel
from modules.utils.LevelDictionary import levelById


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
        
        self.fetchAllUsers = self.db.fetchAllUsers

        self.chapterId = None
        self.levelId = None

        self.title = TextLabel(736, 50, "Leaderboard", 64, (255, 255, 255), screen)
        self.backButton = TextButton(736, 796, "Back", 36, (200, 50, 50), screen)

        self.scoreLabels = []
        self.chapterButtons = []
        self.levelButtons = []

        self.buildChapterButtons()

    def fetchTime(self, timeString):
        mm, ss, cc = timeString.split(":")
        minutes = int(mm)
        seconds = int(ss)
        centis = int(cc)
        return (minutes * 60) + seconds + (centis / 100)

    def enableUi(self, ):
        self.enabled = True

    def disableUi(self):
        self.enabled = False

    def buildChapterButtons(self):
        self.chapterButtons.clear()
        x = 736
        y = 200
        spacing = 80

        for chapterId, chapterData in levelById.items():
            button = TextButton(x, y, chapterData["name"], 36, (200, 50, 50), self.screen)
            self.chapterButtons.append((chapterId, button))
            y += spacing

    def buildLevelButtons(self, chapterId):
        self.levelButtons.clear()
        x = 736
        y = 200
        spacing = 60

        for level in levelById[chapterId]["levels"]:
            levelId = level["id"]
            levelName = level["name"]
            button = TextButton(x, y, levelName, 32, (50, 200, 50), self.screen)
            self.levelButtons.append((chapterId, levelId, button))
            y += spacing

    def buildLeaderboard(self):
        self.scoreLabels.clear()

        users = list(self.fetchAllUsers())
        levelKey = f"{self.chapterId}/{self.levelId}"

        entries = []

        for user in users:
            username = user.get("username")
            levelTimes = user.get("levelTimes", {})

            if levelKey in levelTimes:
                entries.append({
                    "username": username,
                    "timeString": levelTimes[levelKey],
                    "timeSeconds": self.fetchTime(levelTimes[levelKey])
                })

        entries.sort(key=lambda x: x["timeSeconds"])

        y = 200
        for entry in entries:
            label = TextLabel(
                736,
                y,
                f"{entry['username']} - {entry['timeString']}",
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

        if self.chapterId is None:
            for chapterId, button in self.chapterButtons:
                button.draw()

        elif self.levelId is None:
            for chapterId, levelId, button in self.levelButtons:
                button.draw()

        else:
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

                if self.chapterId is None:
                    for chapterId, button in self.chapterButtons:
                        if button.isClicked(event.pos):
                            self.chapterId = chapterId
                            self.buildLevelButtons(chapterId)
                            return
                        
                if self.levelId is None:
                    for chapterId, levelId, button in self.levelButtons:
                        if button.isClicked(event.pos):
                            self.levelId = levelId
                            self.buildLeaderboard()
                            return