# VOID 1680 AM Dashboard

A digital dashboard for the solo playlist building game *VOID 1680 AM* with the *Voices of the Void* expansion.

![on air](https://github.com/user-attachments/assets/ab8f6ca8-f8c5-4eef-a98b-25edb50d93ac)
![off air](https://github.com/user-attachments/assets/7bcd14f1-d674-4b6a-8d63-ebfd8447b968)
![log](https://github.com/user-attachments/assets/cd3b1ba4-b98a-4452-a84d-38386d7b2125)


## Features

### Core Functionality
- **Dual Card Decks**:
  - *Caller Deck*: Draws face cards (J, Q, K, A) from all suits
  - *Playlist Deck*: Draws numbered cards (2-10) with suit filtering
- **Subject**: Shows results for what the caller is calling in for
- **Request**: Shows what the caller is requesting
- **Recallers**: If the caller is calling back, what for and what iteration is their call
- **Block Selection**: Filter Playlist deck by suit (♣ ♦ ♠ ♥) with visual highlighting

### Dynamic Interface
- ON/OFF air toggle with animated switch
- Pulsing radio antenna visualization
- Real-time clock (Local + UTC)
- Animated buttons and effects

### Record Keeping
- Scrollable action log with timestamps
- Persistent history file storage
- Automatic log file generation

## Installation

1. **Recommended**: Download `void1680amdashboard.exe` (Windows executable)
2. **Alternative**: Run `void1680amdashboard.py` with Python 3.12

## Usage Notes

- A log file `VOID_1680_AM_LOG.txt` will be automatically generated in the program directory
- Left mouse click to interact with buttons and switch
- Use mouse wheel to scroll through history

## Technical Details

- Python/Pygame implementation
- Executable file made with PyInstaller
- 1110x480px layout
- Persistent history storage

## Credits

**Code & Design**: Matthew Wrisley  
**Game Concept**: *VOID 1680 AM* and *Voices in the Void* © Bannerless Games (Ken Lowery)  

Created: 14 APR 2025  
Uploaded to GitHub: 16 APR 2025
v2 Update & Upload: 30 APR 2025
