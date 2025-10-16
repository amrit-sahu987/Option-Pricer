import numpy as np
from scipy.stats import norm 
# why does everyone use this norm instead of numpy norm?
# normal distribution not a norm function idiot

#european options
def blackScholes(S, K, T, r, sigma, optionType='call'):
    #should experiment with alpha-stable distributions instead of gaussian
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    try:
        if optionType == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            # think norm defaults to mean 0 std 1
        elif optionType == 'put':
            price = K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return price
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    S = 30 # price of underlying asset
    K = 40 # strike price
    T = 240/252 # time to expiration in years
    r = 0.01 # risk-free interest rate
    sigma = 0.3 # volatility of underlying asset
    optionType = 'call'

    print("Option Price: ", blackScholes(S, K, T, r, sigma, optionType))

if __name__ == '__main__':
    main()

