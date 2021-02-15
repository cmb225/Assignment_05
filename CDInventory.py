# =============================================================================
# Title: CDInventory.py
# Desc: Script for Assignment 05
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# CBuffalow, 2021-Feb-12, Added dicRow variable, replaced menu letters with 
#    capital letters to avoid confusion of 1 vs l, created consistent capitalization 
#    of menu items, added code to section #2, added cd_id generator, added os.path check
# CBuffalow, 2021-Feb-13, added code to all sections, revising comments for clarity
# CBuffalow, 2021-Feb-13, revised Delete section
# CBuffalow, 2021-Feb-14, updated cd_id geneator to find highest ID in data file
#    rather than strictly number of rows
# =============================================================================


# --- DATA --- #

#Loading modules
import os.path

# Declaring variables
strChoice = '' # user input for menu
lstRow = [] # list to hold imported data
lstTbl = []  # list of dictionaries to hold data
newDataOnlyTbl = [] #list of dictionaries to hold data not saved to file
dicRow = {}  # dictionary row of data
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object
objFile_content = '' #empty string for holding file contents
objFile_rows = [] #empty list to hold file contents split into separate strings
indexFinalRow = 0 #index of final row in data file
cd_id = 0 # creating counter for cd_id generator
load = 0 # creating flag to prevent importing file more than once
deleteRow = -1 #creating delete counter for deleting CDs
skipRow = -1 #creating delete counter for deleting CDs



# --- PROCESSING --- #

#counting lines of data in CDInventory.txt so I know where to start next ID number
if os.path.exists(strFileName):
    objFile = open(strFileName, 'r')
    objFile_content = objFile.read() #returns all content of file as a giant string
    objFile.close()
    objFile_rows = objFile_content.split(sep= '\n') #separates data into separate items based on location of \n
    indexFinalRow = len(objFile_rows) -2
    cd_id = int(objFile_rows[indexFinalRow].split(sep= ',')[0])
else:
    cd_id = 0




# --- PRESENTATION (INPUT/OUTPUT) WITH SOME PROCESSING MIXED IN--- #

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
print('The Magic CD Inventory'.center(62))
print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')


while True:  #Display menu of options for user
    print('\t*****MAIN MENU*****')
    print('[L] Load Inventory from file\n[A] Add CD\n[I] Display Current Inventory')
    print('[D] Delete CD from Inventory\n[S] Save Inventory to File\n[X] Exit')
    strChoice = input('L, A, I, D, S or X: ').lower().strip()  # convert choice to lower case at time of input & strips whitespace
    print()
    
    #----------EXIT----------#
    
    if strChoice == 'x': # Exiting the program
        print('\n~~~~~~~~')
        print('Goodbye.')
        print('~~~~~~~~')
        break
    
    #----------LOAD----------#
    
    if strChoice == 'l': # Loading data
        if load == 1: 
            print('\nYou have already loaded the inventory from file. Returning to Main Menu.\n')
            continue
        if os.path.exists(strFileName):

            lstTbl = [] #clearing current inventory as all unsaved cds are saved to newDataOnlyTbl
            objFile = open(strFileName, 'r')
            for row in objFile:
                lstRow = row.strip().split(',')
                dicRow = {'id' : int(lstRow[0]), 'title' : lstRow[1], 'artist' : lstRow[2]}
                lstTbl.append(dicRow)
            objFile.close()
            lstTbl = lstTbl + newDataOnlyTbl #appending new cds to the end of list
            load = 1 #switching flag to 1 so that load process can not be repeated
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Data has been added. Go to "I - Display Current Inventory" to view!')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        else:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('There is no existing inventory to load.')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')


    #----------ADD----------#
    
    elif strChoice == 'a':  # Allowing user to add data to the table as dictionary
        print('~~~~~~~~')
        print('Add a CD')
        print('~~~~~~~~\n')
        dicRow = {} #preventing overwriting as I am using same keys for every dictionary row
        cd_id += 1 
        dicRow['id'] = cd_id
        dicRow['title'] = input('Enter the CD\'s Title: ')
        dicRow['artist'] = input('Enter the Artist\'s Name: ')
        lstTbl.append(dicRow) #adding data to current inventory view
        newDataOnlyTbl.append(dicRow) #adding all unsaved data to a separate table
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Data has been added. Go to "I - Display Current Inventory" to view!')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    
    #----------DISPLAY----------#
    
    elif strChoice == 'i':  # Displaying the current data to the user
        print('~~~~~~~~~~~~~~~~~')
        print('Current Inventory')
        print('~~~~~~~~~~~~~~~~~\n')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        print('{:<5}{:<25}{:<25}'.format('ID', 'CD Title', 'Artist'))
        print()
        for row in lstTbl:
            print('{:<5}{:<25}{:<25}'.format(*row.values()))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    
    #----------DELETE----------#
    
    elif strChoice == 'd': # Providing user the option to delete an entry or cancel
        if len(lstTbl) == 0:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Your current inventory is empty. There are no entries to delete.')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
            continue
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        print('{:<4}\t{:<25}\t{:<25}'.format('ID', 'CD Title', 'Artist'))
        print()
        for row in lstTbl:
            print('{:<4}\t{:<25}\t{:<25}'.format(*row.values()))
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        deleteMe = input('Please enter the ID number of the CD you would like to delete or "0" to Cancel: ')
        try: deleteMe = int(deleteMe.strip()) #testing to see if deleteMe is valid entry that can be cast to int
        except:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('That is not a valid option. Returning to main menu.')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
            continue
        if deleteMe == 0: 
            print('\n~~~~~~~~~~~~~~~~~')
            print('Process Cancelled')
            print('~~~~~~~~~~~~~~~~~\n')
            continue
        for row in lstTbl:
            skipRow += 1
            if deleteMe in row.values():
                deleteRow = skipRow #when match found, row index number transferred to deleteRow variable
                del lstTbl[deleteRow]
                print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('CD #', deleteMe, ' deleted. Go to "I - Display Current Inventory" to view updated inventory!')
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
                break
        if deleteRow == -1: print('\nCD #', deleteMe, ' not found. Returning to Main Menu.\n') #deleteRow will only be "-1" if no match found
        deleteRow = -1 #reseting counters
        skipRow = -1 #reseting counters
    
    
    
    #----------SAVE----------#
    
    elif strChoice == 's':  # Providing user option to save new info or overwite into in CDInventory.txt or cancel
        print("""
Would you like to:
(1) overwrite your saved inventory with your current inventory,
(2) add your new additions to your saved inventory without 
     overwriting the existing contents of the file, or
(3) return to menu?
    
(Note: if you have deleted CDs from the current inventory, these changes will not
       be carried over to your saved file if you choose option 2.)
                """)
        saveType = input('Please enter your selection (1, 2, 3): ')        
        if saveType == '3':  #return to menu
            print()
            continue
        elif saveType == '1':
            objFile = open(strFileName, 'w')
            for row in lstTbl:
                strRow = ''
                for item in row.values():
                    strRow += str(item) + ','
                strRow = strRow[:-1] + '\n'
                objFile.write(strRow)
            objFile.close()
            newDataOnlyTbl = [] #prevents adding albums more than once
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Your data has been saved.')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        elif saveType == '2':  #option to append
            objFile = open(strFileName, 'a')
            for row in newDataOnlyTbl:
                strRow = ''
                for item in row.values():
                    strRow += str(item) + ','
                strRow = strRow[:-1] + '\n'
                objFile.write(strRow)
            objFile.close()
            newDataOnlyTbl = [] #prevents adding albums more than once
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Your data has been saved.')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        else: 
            print('\nThat is not a valid option. Returning to Main Menu.\n')
    
    #----------DEALING W/INCOMPATIBLE INPUT----------#
    
    else: #if user enters invalid menu option
        print('Please choose either L, A, I, D, S or X!\n')

