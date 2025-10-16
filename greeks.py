import numpy as np
from scipy.stats import norm
from blackScholes import blackScholes

# from py_vollib.black_scholes import black_scholes as bs
# from py_vollib.black_scholes.greeks import theta as bs_theta, delta as bs_delta, vega as bs_vega, rho as bs_rho, gamma as bs_gamma, vanna as bs_vanna, volga as bs_volga, charm as bs_charm
# for checking values
# need python 3.10 for that to work

def d1(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma * np.sqrt(T))
    return d1

def d2(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    d2 = d_1 - sigma * np.sqrt(T)
    return d2

def theta(S, K, T, r, sigma, optionType='call'):
    try:
        d_1 = d1(S, K, T, r, sigma)
        d_2 = d2(S, K, T, r, sigma)
        if optionType == 'call':
            theta = (- (S * norm.pdf(d_1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r*T) * norm.cdf(d_2))
        elif optionType == 'put':
            theta = (- (S * norm.pdf(d_1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r*T) * norm.cdf(-d_2))
        return theta
    except Exception as e:
        print(f"Error: {e}")
        return None

def delta(S, K, T, r, sigma, optionType='call'):
    try:
        d_1 = d1(S, K, T, r, sigma)
        if optionType == 'call':
            delta = norm.cdf(d_1)
        elif optionType == 'put':
            delta = -norm.cdf(-d_1) 
        return delta
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def vega(S, K, T, r, sigma, optionType='call'):
    try:
        d_1 = d1(S, K, T, r, sigma)
        vega = S * norm.pdf(d_1) * np.sqrt(T)
        return vega
    except Exception as e:
        print(f"Error: {e}")
        return None

def rho(S, K, T, r, sigma, optionType='call'):
    try:
        d_2 = d2(S, K, T, r, sigma)
        if optionType == 'call':
            rho = K * T * np.exp(-r*T) * norm.cdf(d_2)
        elif optionType == 'put':
            rho = -K * T * np.exp(-r*T) * norm.cdf(-d_2)
        return rho
    except Exception as e:
        print(f"Error: {e}")
        return None

def gamma(S, K, T, r, sigma, optionType='call'):
    try:
        d_1 = d1(S, K, T, r, sigma)
        gamma = norm.pdf(d_1) / (S * sigma * np.sqrt(T))
        return gamma
    except Exception as e:
        print(f"Error: {e}")
        return None

def vanna(S, K, T, r, sigma, optionType='call'):
    try:
        d_2 = d2(S, K, T, r, sigma)
        vega_val = vega(S, K, T, r, sigma, optionType)
        vanna = -vega_val / (S * sigma * np.sqrt(T)) * d_2
        return vanna
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def volga(S, K, T, r, sigma, optionType='call'):
    try:
        d_1 = d1(S, K, T, r, sigma)
        d_2 = d2(S, K, T, r, sigma)
        vega_val = vega(S, K, T, r, sigma, optionType)
        volga = vega_val / sigma * d_1 * d_2
        return volga
    except Exception as e:
        print(f"Error: {e}")
        return None

def charm(S, K, T, r, sigma, optionType='call'):
    pass

def main():
    S = 30 # price of underlying asset
    K = 40 # strike price
    T = 240/252 # time to expiration in years
    r = 0.01 # risk-free interest rate
    sigma = 0.3 # volatility of underlying asset
    optionType = 'call'

    print("Option Price: ", blackScholes(S, K, T, r, sigma, optionType))

    print("Delta: ", delta(S, K, T, r, sigma, optionType))
    # print("Delta (check): ", bs_delta(optionType[0], S, K, T, r, sigma))
    print("Gamma: ", gamma(S, K, T, r, sigma, optionType))
    # print("Gamma (check): ", bs_gamma(optionType[0], S, K, T, r, sigma))
    print("Vega: ", vega(S, K, T, r, sigma, optionType))
    # print("Vega (check): ", bs_vega(optionType[0], S, K, T, r, sigma))  
    print("Theta: ", theta(S, K, T, r, sigma, optionType))
    # print("Theta (check): ", bs_theta(optionType[0], S, K, T, r, sigma))
    print("Rho: ", rho(S, K, T, r, sigma, optionType))
    # print("Rho (check): ", bs_rho(optionType[0], S, K, T, r, sigma))

if __name__ == '__main__':
    main()