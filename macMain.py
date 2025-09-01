import json
import tkinter as tk
from tkinter import font
from datetime import datetime, timedelta
from tkinter import ttk
from tkinter import messagebox


root = tk.Tk()
root.geometry("1400x1000")
root.title("View Database")
editingMode = False
reviewingMode = False
removingMode = False
RecommendedMode = False
root.attributes('-fullscreen', True)

with open("database.json", 'r') as f:
    inventory = json.load(f)

itemContainer = tk.Frame(root)
itemContainer.pack()

def renderInventory():
    """
    for label in itemContainer.winfo_children():
        label.destroy()
    itemLabel = tk.Label(itemContainer, text=f"Name | Review by | In stock", font=font.Font(size=15))
    itemLabel.pack()

    for item in inventory:
        itemLabel = tk.Label(itemContainer, text=f"{item['name']} | {item['reviewDate'][0:2]}/{item['reviewDate'][2:4]}/{item['reviewDate'][4:]} | {item['stockNumber']}", font=font.Font(size=15))
        itemLabel.pack()
        date = datetime(int(item['reviewDate'][4:]), int(item['reviewDate'][2:4]), int(item['reviewDate'][0:2]))
        if (date - datetime.now()).days < 7:
            itemLabel.config(fg="orange")
        if item['stockNumber'] < 2:
            itemLabel.config(fg="red")
    """
    #Code above has been rewritten below for proper table formatting (with borders)
    #yellow is products that need reviewing
    #red is products that are low on stock (below 2)

    for label in itemContainer.winfo_children():
        label.destroy()
    
    nameHeadingBorder = tk.Frame(itemContainer, bg="black")
    nameHeadingBorder.grid(column=1, row=1, sticky="nsew")
    nameHeadingLabel = tk.Label(nameHeadingBorder, text="Name", font=font.Font(weight="bold", size=12))
    nameHeadingLabel.pack(padx=2, pady=2, fill="both")

    reviewDateBorder = tk.Frame(itemContainer, bg="black")
    reviewDateBorder.grid(column=2, row=1, sticky="nsew")
    reviewDateLabel = tk.Label(reviewDateBorder, text="Review by", font=font.Font(weight="bold", size=12))
    reviewDateLabel.pack(padx=2, pady=2, fill="both")

    stockNumBorder = tk.Frame(itemContainer, bg="black")
    stockNumBorder.grid(column=3, row=1, sticky="nsew")
    stockNumLabel = tk.Label(stockNumBorder, text="In stock", font=font.Font(weight="bold", size=12))
    stockNumLabel.pack(padx=2, pady=2, fill="both")

    totalStock = 0

    for i, item in enumerate(inventory):
        print(item['name'])
        totalStock += item['stockNumber']
        date = datetime(int(item['reviewDate'][4:]), int(item['reviewDate'][2:4]), int(item['reviewDate'][0:2]))
        nameCellBorder = tk.Frame(itemContainer, bg="black")
        nameCellBorder.grid(column=1, row=i+2, sticky="nsew")
        nameCell = tk.Label(nameCellBorder, text=item['name'], font=font.Font(size=12))
        nameCell.pack(pady=2,padx=2, fill="both")

        reviewCellBorder = tk.Frame(itemContainer, bg="black")
        reviewCellBorder.grid(column=2, row=i+2, sticky="nsew")
        reviewCell = tk.Label(reviewCellBorder, text=f"{item['reviewDate'][0:2]}/{item['reviewDate'][2:4]}/{item['reviewDate'][4:]}", font=font.Font(size=12))
        reviewCell.pack(pady=2, padx=2, fill="both")

        stockNumCellBorder = tk.Frame(itemContainer, bg="black")
        stockNumCellBorder.grid(column=3, row=i+2, sticky="nsew")
        stockNumCell = tk.Label(stockNumCellBorder, text=str(item['stockNumber']), font=font.Font(size=12))
        stockNumCell.pack(pady=2, padx=2, fill="both")

        def plusOne(itemName):
            for item in inventory:
                if item['name'] == itemName:
                    item['stockNumber'] += 1
                    break
            renderInventory()
        def minusOne(itemName):
            for item in inventory:
                if item['name'] == itemName:
                    item['stockNumber'] -= 1
                    break
            renderInventory()

        plusOneBtn = tk.Button(itemContainer, text="+1", command=lambda itemName=item['name']: plusOne(itemName))
        plusOneBtn.grid(column=4, row=i+2, sticky="nsew")
        minusOneBtn = tk.Button(itemContainer, text="-1", command=lambda itemName=item['name']: minusOne(itemName))
        minusOneBtn.grid(column=5, row=i+2, sticky="nsew")

        if (date - datetime.now()).days < 7:
            nameCell.config(bg="orange")
            reviewCell.config(bg="orange")
            stockNumCell.config(bg="orange")
        if item['stockNumber'] < 2:
            nameCell.config(bg="red")
            reviewCell.config(bg="red")
            stockNumCell.config(bg="red")
    
    totalStockLabelFrame = tk.Frame(itemContainer, bg="black")
    totalStockLabelFrame.grid(column=1,row=i+len(inventory), columnspan=2, sticky="nsew")
    totalStockLabel = tk.Label(totalStockLabelFrame, text="Total Stock:", font=font.Font(weight="bold", size=12))
    totalStockLabel.pack(fill="both", pady=2,padx=2)

    totalStockTextFrame = tk.Frame(itemContainer, bg="black")
    totalStockTextFrame.grid(column=3,row=i+len(inventory), sticky="nsew")
    totalStockText = tk.Label(totalStockTextFrame, text=str(totalStock), font=font.Font(weight="bold", size=12))
    totalStockText.pack(fill="both", pady=2, padx=2)


renderInventory()

def toggleEditing():
    global editingMode
    if not editingMode:
        editingMode = True
        editingWindow = tk.Tk()
        editingWindow.geometry("300x200")
        editingWindow.title("Add to Database")
        editingWindow.attributes('-fullscreen', True)
        editingWindow.attributes('-topmost', True)

        editingWindow.grid_columnconfigure(1, weight=1)
        editingWindow.grid_columnconfigure(2, weight=1)
        editingWindow.grid_columnconfigure(3, weight=1)
        
        nameInputContainer = tk.Frame(editingWindow)
        nameInputContainer.grid(column=2,row=1)

        nameInputLabel = tk.Label(nameInputContainer, text="Name:")
        nameInputLabel.pack(side="left")
        nameInput = tk.Entry(nameInputContainer)
        nameInput.pack(side="right")
        hint = tk.Label(editingWindow, text="Must be DDMMYYYY format")
        hint.grid(column=2, row=4)

        stockInputContainer = tk.Frame(editingWindow)
        stockInputContainer.grid(column=2,row=2)

        stockInputLabel = tk.Label(stockInputContainer, text="In stock:")
        stockInputLabel.pack(side="left")
        stockInput = tk.Entry(stockInputContainer)
        stockInput.pack(side="right")

        reviewDateInputContainer = tk.Frame(editingWindow)
        reviewDateInputContainer.grid(column=2,row=3)

        reviewDateInputLabel = tk.Label(reviewDateInputContainer, text="Review Date:")
        reviewDateInputLabel.pack(side="left")
        reviewDateInput = tk.Entry(reviewDateInputContainer)
        reviewDateInput.pack(side="right")

        #Format DDMMYYYY
        def addItem():
            if len(reviewDateInput.get()) != 8 or not reviewDateInput.get().isdigit():
                messagebox.showerror("Invalid Date", "Review date must be in DDMMYYYY numerical format.", parent=editingWindow)
                return
            inventory.append({'name': nameInput.get(), 'reviewDate': reviewDateInput.get(), 'stockNumber': int(stockInput.get())})
            nameInput.delete(0, tk.END)
            stockInput.delete(0, tk.END)
            reviewDateInput.delete(0, tk.END)
        
        add = tk.Button(editingWindow, text="Add", bg="green", command=addItem)
        add.grid(column=2, pady=5)

        def close():
            global editingMode
            with open("database.json", 'w') as f:
                json.dump(inventory, f, indent=4)
            editingWindow.destroy()
            renderInventory()
            editingMode = False

        close = tk.Button(editingWindow, text="Save & Close", command=close)
        close.grid(sticky="s", pady=5, column=2)

        def onClose():
            with open("database.json", 'w') as f:
                json.dump(inventory, f, indent=4)
            editingMode = False
            renderInventory()
            editingWindow.destroy()
    
        editingWindow.protocol("WM_DELETE_WINDOW", onClose)

        editingWindow.mainloop()

editModeButton = tk.Button(root, text="Enter Addition Mode", command=toggleEditing)
editModeButton.pack()

def toggleReviewing():
    global reviewingMode
    if not reviewingMode:
        reviewingMode = True
        reviewingWindow = tk.Tk()
        reviewingWindow.geometry("1400x1000")
        reviewingWindow.title("Reviewing Mode")
        reviewingWindow.attributes('-fullscreen', True)
        reviewingWindow.attributes('-topmost', True)

        itemContainer = tk.Frame(reviewingWindow)
        itemContainer.pack()

        def reviewed(name):
            print(name)
            for item in inventory:
                if item['name'] == name:
                    day = item['reviewDate'][0:2]
                    month = item['reviewDate'][2:4]
                    year = item['reviewDate'][4:]
                    try:
                        newDate = datetime(int(year) + 1, int(month), int(day))
                    except ValueError:
                        if int(month) == 2 and int(day) == 29:
                            newDate = datetime(int(year) + 1, 2, 28)
                        else:
                            raise
                        
                    item['reviewDate'] = f"{newDate.day:02d}{newDate.month:02d}{newDate.year}"
                    break
            revRender()

        def revRender():
            for item in itemContainer.winfo_children():
                item.destroy()
            for i, item in enumerate(inventory):
                itemLabelBorder = tk.Frame(itemContainer, bg="black")
                itemLabelBorder.grid(row=i+1, column=1, sticky="nsew")
                itemLabel = tk.Label(itemLabelBorder, text=f"{item['name']} | {item['reviewDate'][0:2]}/{item['reviewDate'][2:4]}/{item['reviewDate'][4:]} | {item['stockNumber']}", font=font.Font(size=15))
                itemLabel.pack(fill="both", padx=2, pady=2)
                date = datetime(int(item['reviewDate'][4:]), int(item['reviewDate'][2:4]), int(item['reviewDate'][0:2]))
                if (date - datetime.now()).days < 7:
                    itemLabel.config(bg="orange")
                reviewButton = tk.Button(itemContainer, text="Mark as reviewed (+1 year)", bg="green", command=lambda name=item['name']: reviewed(name))
                reviewButton.grid(row=i+1, column=2)
        revRender()
        def close():
            global reviewingMode
            with open("database.json", 'w') as f:
                json.dump(inventory, f, indent=4)
            reviewingWindow.destroy()
            renderInventory()
            reviewingMode = False

        close = tk.Button(reviewingWindow, text="Save & Close", command=close)
        close.pack(pady=5)

        def onClose():
            with open("database.json", 'w') as f:
                json.dump(inventory, f, indent=4)
            reviewingMode = False
            renderInventory()
            reviewingWindow.destroy()
    
        reviewingWindow.protocol("WM_DELETE_WINDOW", onClose)



reviewingModeButton = tk.Button(root, text="Enter Reviewing mode", command=toggleReviewing)
reviewingModeButton.pack()

def toggleRemoving():
    global removingMode
    if not removingMode:
        removingMode = True
        
        removingWindow = tk.Tk()
        removingWindow.geometry("1400x1000")
        removingWindow.title("Removing from database")
        removingWindow.attributes('-fullscreen', True)
        removingWindow.attributes('-topmost', True)

        itemContainer = tk.Frame(removingWindow)
        itemContainer.pack()

        def renderItems():
            for label in itemContainer.winfo_children():
                label.destroy()
            nameHeadingBorder = tk.Frame(itemContainer, bg="black")
            nameHeadingBorder.grid(column=1, row=1, sticky="nsew")
            nameHeadingLabel = tk.Label(nameHeadingBorder,  text="Name", font=font.Font(weight="bold", size=12))
            nameHeadingLabel.pack(padx=2, pady=2, fill="both")

            reviewDateBorder = tk.Frame(itemContainer, bg="black")
            reviewDateBorder.grid(column=2, row=1, sticky="nsew")
            reviewDateLabel = tk.Label(reviewDateBorder, text="Review by",  font=font.Font(weight="bold", size=12))
            reviewDateLabel.pack(padx=2, pady=2, fill="both")

            stockNumBorder = tk.Frame(itemContainer, bg="black")
            stockNumBorder.grid(column=3, row=1, sticky="nsew")
            stockNumLabel = tk.Label(stockNumBorder, text="In stock",  font=font.Font(weight="bold", size=12))
            stockNumLabel.pack(padx=2, pady=2, fill="both")

            removeHeadingBorder = tk.Frame(itemContainer, bg="black")
            removeHeadingBorder.grid(column=4, row=1, sticky="nsew")
            removeHeadingLabel = tk.Label(removeHeadingBorder, text="Remove Item", font=font.Font(weight="bold", size=12))
            removeHeadingLabel.pack(padx=2, pady=2, fill="both")

            for i, item in enumerate(inventory):
                date = datetime(int(item['reviewDate'][4:]), int(item['reviewDate'][2:4]), int(item['reviewDate'][0:2]))
                nameCellBorder = tk.Frame(itemContainer, bg="black")
                nameCellBorder.grid(column=1, row=i+2, sticky="nsew")
                nameCell = tk.Label(nameCellBorder, text=item['name'],  font=font.Font(size=12))
                nameCell.pack(pady=2,padx=2, fill="both")

                reviewCellBorder = tk.Frame(itemContainer, bg="black")
                reviewCellBorder.grid(column=2, row=i+2, sticky="nsew")
                reviewCell = tk.Label(reviewCellBorder, text=f"{item['reviewDate'][0:2]}/{item['reviewDate'][2:4]}/{item['reviewDate'][4:]}", font=font.Font(size=12))
                reviewCell.pack(pady=2, padx=2, fill="both")

                stockNumCellBorder = tk.Frame(itemContainer, bg="black")
                stockNumCellBorder.grid(column=3, row=i+2, sticky="nsew")
                stockNumCell = tk.Label(stockNumCellBorder, text=str(item['stockNumber']), font=font.Font(size=12))
                stockNumCell.pack(pady=2, padx=2, fill="both")

                def removeItem(itemName):
                    for i, item in enumerate(inventory):
                        if item['name'] == itemName:
                            inventory.pop(i)
                    renderItems()

                removeButtonCell = tk.Button(itemContainer, bg="red", text="Remove", command=lambda itemName=item['name']: removeItem(itemName))
                removeButtonCell.grid(column=4, row=i+2, sticky="nsew")

                if (date - datetime.now()).days < 7:
                    nameCell.config(bg="orange")
                    reviewCell.config(bg="orange")
                    stockNumCell.config(bg="orange")
                if item['stockNumber'] < 2:
                    nameCell.config(bg="red")
                    reviewCell.config(bg="red")
                    stockNumCell.config(bg="red")

        renderItems()
        
        def saveAndQuit():
            global removingMode
            with open("database.json", 'w') as f:
                json.dump(inventory, f, indent=4)

            removingWindow.destroy()
            renderInventory()
            removingMode = False

        saveAndQuitBtn = tk.Button(removingWindow, text="Save & Quit", command=saveAndQuit)
        saveAndQuitBtn.pack()

        def onClose():
            global reviewingMode
            with open("database.json", 'w') as f:
                json.dump(inventory, f, indent=4)
            removingMode = False
            renderInventory()
            removingWindow.destroy()
    
        removingWindow.protocol("WM_DELETE_WINDOW", onClose)  

removingModeButton = tk.Button(root, text="Enter Removing Mode", command=toggleRemoving)
removingModeButton.pack()

def RecommendedNextOrder():
    global RecommendedMode
    if not RecommendedMode:
        RecommendedMode = True
        recommendedWindow = tk.Tk()
        recommendedWindow.title("Recommended next order")
        recommendedWindow.attributes('-fullscreen', True)
        recommendedWindow.attributes('-topmost', True)
        recommendedOrder = []

        title = tk.Label(recommendedWindow, text="Recommended next order:", font=font.Font(size=20, weight="bold"))
        title.pack()

        for item in inventory:
            if item['stockNumber'] < 5:
                recommendedOrder.append(item)
        recItemsContainer = tk.Frame(recommendedWindow)
        recItemsContainer.pack()
        
        nameHeaderBorder = tk.Frame(recItemsContainer, bg="black")
        nameHeaderBorder.grid(column=1, row=1, sticky="nsew")
        nameHeader = tk.Label(nameHeaderBorder, text="Name",  font=font.Font(size=12, weight="bold"))
        nameHeader.pack(fill="both", padx=2, pady=2)
        
        stockHeaderBorder = tk.Frame(recItemsContainer, bg="black")
        stockHeaderBorder.grid(column=2, row=1, sticky="nsew")
        stockHeader = tk.Label(stockHeaderBorder, text="In stock",  font=font.Font(size=12, weight="bold"))
        stockHeader.pack(fill="both", padx=2, pady=2)

        for i, item in enumerate(recommendedOrder):
            nameLabelBorder = tk.Frame(recItemsContainer, bg="Black")
            nameLabelBorder.grid(column=1, row=i+2, sticky="nsew")
            nameLabel = tk.Label(nameLabelBorder, text=item['name'], font=font.Font(size=12))
            nameLabel.pack(fill="both", padx=2, pady=2)

            stockLabelBorder = tk.Frame(recItemsContainer, bg="Black")
            stockLabelBorder.grid(column=2, row=i+2, sticky="nsew")
            stockLabel = tk.Label(stockLabelBorder, text=str(item['stockNumber']),  font=font.Font(size=12))
            stockLabel.pack(fill="both", padx=2, pady=2)

        def close():
            global RecommendedMode
            RecommendedMode = False
            recommendedOrder.clear()
            recommendedWindow.destroy()

        closeBtn = tk.Button(recommendedWindow, text="Close", command=close)
        closeBtn.pack(pady=5)

        recommendedWindow.protocol("WM_DELETE_WINDOW", close)


recNextOrderButton = tk.Button(root, text="View Recommended next order", command=RecommendedNextOrder)
recNextOrderButton.pack()

def onClose():
    with open("database.json", 'w') as f:
        json.dump(inventory, f, indent=4)
    root.destroy()
    
root.protocol("WM_DELETE_WINDOW", onClose)

mainCloseBtn = tk.Button(root, text="Save & Quit", command=onClose)
mainCloseBtn.pack(side="bottom", pady=(0,10))

root.mainloop()