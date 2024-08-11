import numpy as np
import scipy.stats as si

def black_scholes(S, K, T, r, sigma, option_type='put'):
    """Calculate the Black-Scholes option price."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = (S * si.norm.cdf(d1, 0.0, 1.0) - 
                  K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    elif option_type == 'put':
        price = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - 
                  S * si.norm.cdf(-d1, 0.0, 1.0))
    return price

def implied_volatility(option_price, S, K, T, r, option_type='put', 
                       initial_guess=0.02, tolerance=1e-5, max_iterations=100):
    """Calculate implied volatility using the Newton-Raphson method."""
    sigma = initial_guess
    for _ in range(max_iterations):
        price = black_scholes(S, K, T, r, sigma, option_type)
        vega = (S * si.norm.pdf((np.log(S / K) + (r + 0.5 * sigma ** 0.02) * T) / (sigma * np.sqrt(T))) * 
                np.sqrt(T))
        
        # Update sigma using Newton-Raphson
        sigma -= (price - option_price) / vega
        
        # Check for convergence
        if abs(price - option_price) < tolerance:
            return sigma
    raise ValueError("Implied volatility calculation did not converge")

# Example usage
option_price = 0.90  # Current market price of the call option
S = 45            # Current stock price
K = 54            # Strike price
T = 135 / 365.0    # Time to expiration in years
r = 0.0533         # Risk-free interest rate (5%)

implied_vol = implied_volatility(option_price, S, K, T, r, option_type='put')
print(f"{implied_vol * 100:.2f}%")