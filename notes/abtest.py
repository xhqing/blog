from statsmodels.stats.power import zt_ind_solve_power
from statsmodels.stats.proportion import proportion_effectsize as es
 
r = zt_ind_solve_power(effect_size=es(prop1=0.70, prop2=0.705), alpha=0.05, power=0.8, alternative="two-sided")
print(r)
