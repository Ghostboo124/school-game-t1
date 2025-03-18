import pygame

class MusicManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_song = None
        self.loops = 0
        self.queue = []
        # Set an event to be triggered when the music ends
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

    def loadAndPlay(self, music_file: str, namehint: str = "", loops: int = 0):
        self.loops = loops
        # Load the music file
        pygame.mixer.music.load(music_file, namehint)
        # Play the music
        pygame.mixer.music.play(self.loops)
        # Store the current song name
        self.current_song = namehint
        # Clear the queue
        self.queue.clear()

    def queue(self, music_file, namehint):
        # Queue the music file
        pygame.mixer.music.queue(music_file, namehint)
        # Append the namehint to the queue
        self.queue.append(namehint)

    def getSong(self):
        return self.current_song

    def getQueue(self):
        return self.queue

    def updateSong(self):
        if self.queue:
            self.current_song = self.queue.pop(0)
        else:
            self.current_song = None

    def pause(self) -> None:
        if self.getSong != None:
            return pygame.mixer.music.pause()
        return
    
    def play(self) -> None:
        if self.getSong != None:
            return pygame.mixer.music.unpause()
        return