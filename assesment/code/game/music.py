import pygame

class MusicManager:
    def __init__(self):
        pygame.mixer.init()
        self.currentSong: str | None = None
        self.loops = 0
        self.queue: list[str] = []
        # Set an event to be triggered when the music ends
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

    def loadAndPlay(self, music_file: str, namehint: str = "", loops: int = 0) -> None:
        self.loops: int = loops
        # Load the music file
        pygame.mixer.music.load(music_file, namehint)
        # Play the music
        pygame.mixer.music.play(self.loops)
        # Store the current song name
        self.currentSong = namehint
        # Clear the queue
        self.queue.clear()

    def queueSong(self, music_file, namehint) -> None:
        # Queue the music file
        pygame.mixer.music.queue(music_file, namehint)
        # Append the namehint to the queue
        self.queue.append(namehint)

    def getSong(self) -> str:
        if isinstance(self.currentSong, str):
            return self.currentSong
        else:
            return "No song playing."

    def getQueue(self) -> list[str]:
        return self.queue

    def updateSong(self) -> None:
        if self.queue:
            self.currentSong = self.queue.pop(0)
        else:
            self.currentSong = None

    def pause(self) -> None:
        if self.getSong != None:
            return pygame.mixer.music.pause()
        return
    
    def play(self) -> None:
        if self.getSong != None:
            return pygame.mixer.music.unpause()
        return