import numpy as np
import matplotlib.pyplot as plt
# plt.style.use('ggplot')
# plt.style.use('seaborn-darkgrid')


from blackScholes import blackScholes
from greeks import theta, delta, vega, rho, gamma, vanna, volga, charm

def decomposition(S, K, T, r, sigma, dS, dSigma, dR, dT, optionType='call'):
    try:
        price_0 = blackScholes(S, K, T, r, sigma, optionType)
        theta_val = theta(S, K, T, r, sigma, optionType)
        delta_val = delta(S, K, T, r, sigma, optionType)
        vega_val = vega(S, K, T, r, sigma, optionType)
        rho_val = rho(S, K, T, r, sigma, optionType)
        gamma_val = gamma(S, K, T, r, sigma, optionType)
        vanna_val = vanna(S, K, T, r, sigma, optionType)
        volga_val = volga(S, K, T, r, sigma, optionType)
        # charm_val = charm(S, K, T, r, sigma, optionType)
        price_1 = blackScholes(S + dS, K, T + dT, r + dR, sigma + dSigma, optionType)

        dPrice = price_1 - price_0

        print(f"Initial Price: {price_0}")
        print(f"New Price after changes: {price_1}")
        print(f"Change in Price: {dPrice}")
        
        theta_term = theta_val * dT
        delta_term = delta_val * dS # think this assumes delta hedging?
        vega_term = vega_val * dSigma
        rho_term = rho_val * dR
        gamma_term = 0.5 * gamma_val * dS**2
        vanna_term = vanna_val * dS * dSigma
        volga_term = 0.5 * volga_val * dSigma**2
        # charm_term = charm_val * dT

        total_greeks = (
        delta_term
        + gamma_term
        + vega_term
        + volga_term
        + vanna_term
        + rho_term
        + theta_term
        # + charm_term
        )

        residual = dPrice - total_greeks

        results = {
        "Delta": delta_term,
        "Gamma": gamma_term,
        "Vega": vega_term,
        "Volga": volga_term,
        "Vanna": vanna_term,
        "Rho": rho_term,
        "Theta": theta_term,
        # "Charm": charm_term,
        "Total (Greeks)": total_greeks,
        "Actual ΔP": dPrice,
        "Residual": residual,
        }
        return results

    except Exception as e:
        print(f"Error in decomposition: {e}")
        return None

def plot(results):
    fig = plt.figure(figsize=(15, 5))
    x = list(results.keys())
    y = list(results.values())
    plt.bar(x, y)
    plt.title("P&L Decomposition")
    plt.show()


def main():
    S = 30 # price of underlying asset
    K = 40 # strike price
    T = 240/252 # time to expiration in years (252 trading days in a year)
    r = 0.01 # risk-free interest rate
    sigma = 0.3 # volatility of underlying asset
    optionType = 'call'

    dS = 0.5
    dSigma = 0.01
    dR = 0.0005
    dT = -1/252

    results = decomposition(S, K, T, r, sigma, dS, dSigma, dR, dT, optionType)
    plot(results) # why is total of greeks slightly more than actual dP?

if __name__ == '__main__':
    main()