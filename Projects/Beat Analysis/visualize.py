import pygame
import WAVFile as wav
#from math import pi
#import alsaaudio as alsa

'''
    Creates a simple window with a green circle
    Plays the song (contained in wf)
    Makes the circle flash red according to the data (for 200 ms)

    data: expected to be a list containing indexes of samples
    where the beat occurs

    wf: WAVFile containg the song
'''
def visualize(data, wf):
    # Initialize the game engine
    pygame.init()

    # Define the colors we will use in RGB format
    BLACK = (  0,   0,   0) #unused
    WHITE = (255, 255, 255) #unused
    BLUE =  (  0,   0, 255) #unused
    GREEN = ( 51, 255,  85)
    RED =   (255,   0,   0)
    BEAT1 = ( 14, 102,  85) #unused
    BEAT = RED
     
    # Set the height and width of the screen
    size = [400, 300]
    screen = pygame.display.set_mode(size)
     
    pygame.display.set_caption("Feel the beat")

    # start counting the time
    clock = pygame.time.Clock() # in ms
    
    # Clear the screen and set the screen background
    screen.fill(WHITE)
    pygame.draw.circle(screen, GREEN, [200, 150], 40)
    pygame.display.flip()

    # start playing the song
    pygame.mixer.music.load(wf.fileName)
    pygame.mixer.music.play()
    
    curr_index = 0
    beat = False # are we currently inside a beat?
    sampleFreq = 1000000/wf.sampleRate # in ms
    done = False # to end the for loop by force 
    beat_timer = 0 # stores for how long the current beat is being displayed
    elapsed_time = 0 # stores the ttime since beginning
    for sample in range(0,wf.numSamples,1000):
        beat_timer += elapsed_time
        elapsed_time = clock.tick()
        beat_timer += elapsed_time

        if done:
            break
        
        if beat and beat_timer > 200: # if the beat time has expired
            screen.fill(WHITE)
            pygame.draw.circle(screen, GREEN, [200, 150], 40)
            pygame.display.flip()
            beat = False

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
                
        #while elapsed_time < sampleFreq:
        #    elapsed_time += clock.tick()

        # if we are currently at the sample which contains beat    
        if curr_index<data.__len__() and data[curr_index] <= sample:
            screen.fill(WHITE)
            pygame.draw.circle(screen, BEAT, [200, 150], 40)
            pygame.display.flip()
            beat = True
            beat_timer = 0
            curr_index += 1
            
        # print out each second
        # only works for 44100Hz songs 
        if sample%44000 == 0:
            print (str(sample//44000) + ' secs')

        # wait until the next samples
        # to match the song being played
        while elapsed_time < sampleFreq:
            elapsed_time += clock.tick()

    print ("the end of for loop")
        
    # Be IDLE friendly
    pygame.quit()
    
'''
    Obsolete function
    Unused
'''
def drawBeat(screen):
    # Clear the screen and set the screen background
    screen.fill(WHITE)
    # Draw a circle
    pygame.draw.circle(screen, BEAT, [200, 150], 40)
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(5)
    screen.fill(WHITE)

'''
    Convert data in format of indexes of samples containing beats
    into timestamps and write them to a file

    Used to view data in Audacity
'''
def labels(out_file, wf, data):
    out = open(out_file, 'w')
    for sample in data:
        time = sample/wf.sampleRate
        out.write(str(time))
        out.write('\t')
        out.write(str(time))
        out.write('\t')
        out.write('B')
        out.write('\n')
    out.close()

