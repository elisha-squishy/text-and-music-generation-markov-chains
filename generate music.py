import music21
import pygame
import random

# Initialize pygame for MIDI playback
pygame.mixer.init()
MIDI_FILE = "C:/Users/robin/OneDrive/Documents/projects/computer projects/music_file.mid"
def play_musicxml(file_path):
    # Parse the .mxl file using music21
    score = music21.converter.parse(file_path)
    #score.show()
    score.write('midi', fp=MIDI_FILE)
    play_song()

def parse_score(file_path):
    # Parse the MusicXML file
    score = music21.converter.parse(file_path)

    # Flatten the score to get all elements in a single iterable
    flattened_score = score.flat

    # Iterate over all elements in the flattened score
    #my_elements={}
    my_score=[]
    for element in flattened_score:
        if isinstance(element, music21.note.Note):
            my_score.append((element.nameWithOctave, element.quarterLength),)
            
            '''
            if element.offset not in my_elements:
            
                my_elements[element.offset]=[(element.nameWithOctave, element.quarterLength)]
            else:
                my_elements[element.offset].append((element.nameWithOctave, element.quarterLength))
                '''
        elif isinstance(element, music21.metadata.Metadata):
            print(f"Metadata - Title: {element.title}, Composer: {element.composer}")
            #print(f"Note: {element.nameWithOctave}, Duration: {element.quarterLength}, Offset: {element.offset}")
        '''
        elif isinstance(element, music21.note.Rest):
            pass
            #print(f"Rest, Duration: {element.quarterLength}, Offset: {element.offset}")
        elif isinstance(element, music21.chord.Chord):
            notes = [n.nameWithOctave for n in element.notes]
            #print(f"Chord: {', '.join(notes)}, Duration: {element.quarterLength}, Offset: {element.offset}")
        '''
    '''
    my_score=[]
    
    for i in my_elements:
        #my_score+=tuple(my_elements[i], )
        my_score.append(my_elements[i])
   '''
    return my_score
def markov_train(lookForward, my_score):
    chain={}
    
    i=0 

    while(i<(len(my_score)-lookForward-1)):
        score_slice_curr = tuple(my_score[i:i+lookForward])

        score_slice_next = tuple(my_score[i+lookForward:i+2*lookForward])
        if score_slice_curr not in chain:
            chain[score_slice_curr]={}      #add a new key
            
        if score_slice_next in chain[score_slice_curr]:
            chain[score_slice_curr][score_slice_next] += 1   #current group of letters is followd by next group of letters
        else:
            chain[score_slice_curr][score_slice_next]=1
        i+=1
    for i in chain:
        total=0 
        for  value in chain[i].values():
            total+=value
        #print(total)
        if total!=0:
            #print(chain[i].values())
            for  key in chain[i].keys():
                chain[i][key]/=total
    return (chain)

def generate_music(chain, length):
    score = music21.stream.Score()
    part = music21.stream.Part()
    prompt = random.choice(list(chain.keys()))
    cumulative_offset = 0

    for _ in range(length):
        for note_name, note_duration in prompt:
            note = music21.note.Note(note_name)
            note.quarterLength = note_duration
            note.offset = cumulative_offset   
            part.append(note)
            cumulative_offset += note_duration  

        rnd = random.random()
        counter = 0
        total = sum(chain[prompt].values())  
        for key, value in chain[prompt].items():
            counter += value / total  
            if counter >= rnd:
                prompt = key  
                break

    score.append(part)
    score.show()
def play_song():
    pygame.mixer.music.load(MIDI_FILE)
    pygame.mixer.music.play()
    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Provide the path to your .mxl file
file_path = "C:/Users/robin/Downloads/Spring-Four_seasons_vivaldi.mxl"
#play_musicxml(file_path)
my_score=parse_score(file_path)
chain=markov_train(1, my_score)
generate_music(chain, 100)