class Category:

  ledger = []
  category = ""

  #Initializes the object and assign value to the variable category
  def __init__(self, category):
    self.category = category
  #Prints a receipt with data of the category instance, transaction description and total balance
  def __str__(self):
    receipt = ""
    total_amount = self.get_balance()
    #Header section of the receipt 
    section_length = ((30 - len(self.category)) / 2)
    while section_length != 0:
      receipt += '*'
      section_length = section_length - 1

    receipt += self.category

    while len(receipt) < 30:
      receipt += '*'
    receipt += '\n'
    #Body section of the receipt
    for transaction in self.ledger:
      if transaction['category'] == self.category:

        receipt += transaction['description'][0:23]
        transaction_amount = '{:.2f}'.format(transaction['amount'])
        if len(transaction['description']) < 23:
          receipt += transaction_amount.rjust(30 -
                                              len(transaction['description']))
        else:
          receipt += transaction_amount.rjust(7)
        receipt += '\n'
    #Total balance of the receipt
    receipt += 'Total: ' + '{:.2f}'.format(total_amount)

    return receipt

  #Checks if the funds are higher than the input amount
  def check_funds(self, amount):
    if self.get_balance() < amount:
      return False
    else:
      return True

  # Returns the total balance of the transaction in the category 
  def get_balance(self):
    total_balance = 0
    for transaction in self.ledger:
      if self.category == transaction["category"]:
        total_balance += transaction['amount']

    return total_balance

  #Adds a new deposit transaction to the ledger list
  def deposit(self, amount, description):
    self.ledger.append({
      "amount": amount,
      "description": description,
      "category": self.category
    })

  #Adds a new withdraw transaction into the ledger
  #The description argument is set to 'No description' by default
  def withdraw(self, amount, description='No description'):

    if self.check_funds(amount) == False:
      return False
    else:
      self.ledger.append({
        "amount": -amount,
        "description": description,
        "category": self.category
      })
      return True
  #Makes a transfer operation, Adding a withdrawal transaction to the current instance, and making a deposit in the transfered instance
  def transfer(self, amount, category):

    original_category = self.category
    withdraw_message = "Transfer to " + str(category)
    income_message = "Transfer from " + self.category

    if self.check_funds(amount) == False:
      return False
    else:
      self.withdraw(amount, withdraw_message)
      self.category = category
      self.deposit(amount, income_message)
      self.category = original_category
      
      return True

#Spending chart showing the percentages of spending by category
def create_spend_chart(categories):
  
  chart = "Percentage spend by category\n"
  # Creates the percentage axis 
  percentage_counter = 100
  while percentage_counter >= 0:
    chart += str(percentage_counter).rjust(3) + '| '
    #calculates the percentage of spending by category
    for instance in categories:
      
      full_expences = 0
      category_expences = 0
      
      for transaction in instance.ledger:
        is_transfer = transaction["description"].split(' ')[0]
        if transaction["category"] == instance.category and transaction[
            "amount"] < 0 and is_transfer != "Transfer":
          category_expences += transaction["amount"]
      for transaction in instance.ledger:
        is_transfer = transaction["description"].split(' ')[0]
        if transaction["amount"] < 0 and is_transfer != "Transfer":
          full_expences += transaction["amount"]
     
      percentage = (category_expences / full_expences) * 100
      rounded_percentage = round(percentage / 10) * 10
      #Writes 'o' if the category has that percentage or ' ' if not
      if rounded_percentage >= percentage_counter:
        chart += 'o  '
      else:
        chart += '   '
    chart += '\n'
    percentage_counter = percentage_counter - 10
  #separation bar 
  chart += '    '
  chart += '----------'
  chart += '\n'
  chart += '     '
  #writes the titles below the chart
  largest_categorie = 0
  for instance in categories:
    if len(instance.category) > largest_categorie:
      largest_categorie = len(instance.category)

  string_crawler = 0
  while largest_categorie >= 0:

    for instance in categories:
      try:
        chart += instance.category[string_crawler] + '  '
      except IndexError:
        chart += '   '
    chart += '\n'
    chart += '     '
    string_crawler += 1
    largest_categorie = largest_categorie - 1

  print(chart)




