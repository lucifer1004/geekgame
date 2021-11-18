from itertools import combinations
from fractions import *
  
def peace(xr, xc, yr, yc):
  if xr == yr:
    return False
  if xc == yc:
    return False
  if xr - xc == yr - yc:
    return False
  if xr + xc == yr + yc:
    return False
  return True
  
def brute_force(row, col):
  ans = 0
  for x, y, z in combinations(range(row * col), 3):
    xr, xc = x // col, x % col
    yr, yc = y // col, y % col
    zr, zc = z // col, z % col
    if peace(xr, xc, yr, yc) and peace(xr, xc, zr, zc) and peace(yr, yc, zr, zc):
      ans += 1
  return ans

  
def F(m, n):
  if m > n:
    m, n = n, m
    
  assert(n >= 3)
  
  return Fraction(n**3,6)*(m**3 - 3*m**2 + 2*m) - Fraction(n**2,2)*(3*m**3 - 9*m**2 + 6*m) + Fraction(n,6)*(2*m**4 + 20*m**3 - 77*m**2 + 58*m) - Fraction(1, 24)*(39*m**4 - 82*m**3 - 36*m**2 + 88*m) + Fraction(1, 16)*(2*m - 4*n + 1)*(1 + (-1)**(m+1)) + Fraction(1,2)*(1 + abs(n - 2*m + 3) - abs(n - 2*m + 4))*(Fraction(1, 24)*((n - 2*m + 11)**4 - 42*(n - 2*m + 11)**3 + 656*(n - 2*m + 11)**2 - 4518*(n - 2*m + 11) + 11583) - Fraction(1, 16)*(4*m - 2*n - 1)*(1 + (-1)**(n+1))) 

row = 672328094
col = 386900246

print(F(row, col))