try:
    from rich.table import Table
    import math
    from rich.console import Console
    import argparse
    import random
except ImportError as ie:
    print("Error: missing modules", ie)
    exit(1)


def dataInput():
    parser = argparse.ArgumentParser()
    parser.add_argument("value", help="Loan value")
    parser.add_argument("commission", help="Bank's commission")
    parser.add_argument("interest", help="Current bank's interest")
    parser.add_argument("months", help="Loan term in months")

    try:
        args = parser.parse_args()
    except argparse.ArgumentError or argparse.ArgumentTypeError:
        print("Error: wrong input arguments")
        exit(1)

    value = float(args.value)
    commission = float(args.commission)
    interest = float(args.interest)
    months = int(args.months)

    loanData = (value, commission, interest, months)
    if len(loanData) < 4:
        print("Error: not enough loan data")
        exit(1)
    return loanData

def dataChecker(loanData):
    for i in range (len(loanData)):
        if loanData[i] <= 0 or math.isnan(loanData[i]) == True:
            print("Error: wrong input arguments")
            exit(1)
        elif loanData[1] > 100 or loanData[2] > 100:
            print("Error: commission and interest cannot be greater than 100")
            exit(1)
        else:
            i +=0
    return loanData

def interestVolatilityModel(loanData):
    interestModel = [loanData[2]]
    volatility = 3
    for k in range(loanData[3]):
        interestTemp = loanData[2] + round(random.normalvariate(0, volatility),2)
        if interestTemp <=0:
            continue
        interestModel.append(interestTemp)
        interestModel.append(interestTemp)
        interestModel.append(interestTemp)
        interestModel.append(interestTemp)

    return interestModel


def calculateTotalInstallment(loanData, currentInterest):
    totalInstallmentNumerator = (loanData[0] * ((currentInterest*0.01) / 12) * (1 + ((currentInterest*0.01) / 12)) ** loanData[3])
    totalInstallmentDenominator = ((1 + (currentInterest*0.01 / 12)) ** loanData[3]) - 1
    totalInstallment = round((totalInstallmentNumerator / totalInstallmentDenominator), 2)

    return totalInstallment

def calculateInterestInstallment(loanData, remaining, currentInterest):
    interestInstallment = round(remaining * ((currentInterest*0.01)/12), 2)
    return interestInstallment

def calculateCapitalInstallment(totalInstallment, interestInstallment):
    capitalInstallment = round((totalInstallment - interestInstallment), 2)
    return capitalInstallment



def schedulePayment(loanData, interestModel):
    installmentsList = [[] for i in range(loanData[3])]
    totalInstallment = 0
    remaining = loanData[0]
    for k in range(len(interestModel)):
        currentInterest = interestModel[k]
        for i in range(loanData[3]):
            totalInstallment = calculateTotalInstallment(loanData, currentInterest)
            interestInstallment = calculateInterestInstallment(loanData, remaining, currentInterest)
            capitalInstallment = calculateCapitalInstallment(totalInstallment, interestInstallment)
            installmentsList[i].append(i)
            installmentsList[i].append(totalInstallment)
            installmentsList[i].append(capitalInstallment)
            installmentsList[i].append(interestInstallment)
            installmentsList[i].append(remaining)
            remaining = round((remaining - capitalInstallment), 2)
    return installmentsList
    

def formTable(installmentsList):
    table = Table(title = "Payment schedule")
    console = Console()


    table.add_column("Inst. number", style="green")
    table.add_column("Total inst. value", style="cyan")
    table.add_column("Capital inst. value", style="blue")
    table.add_column("Interest inst. value", style="magenta")
    table.add_column("Remaining", style="red")

    for i in range(len(installmentsList)):
        table.add_row(str(i + 1), str(installmentsList[i][1]), str(installmentsList[i][2]),
         str(installmentsList[i][3]), str(installmentsList[i][4]))
            
    console.print(table)


def main():
    loanData = dataInput()
    dataChecker(loanData)
    interestModel = interestVolatilityModel(loanData)
    installmentsList = schedulePayment(loanData, interestModel)
    formTable(installmentsList)
    return 0

if __name__ == "__main__":
    main()
