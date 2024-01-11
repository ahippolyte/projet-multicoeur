### histogram_omp_outer

#### Avantages
- Peut bénéficier de ```break``` qui économise plusieurs itérations
- Génération d'une unique équipe de threads
#### Inconvénients
- Nécéssité de l'instruction atomique (couteuse)

### histogram_omp_inner

#### Avantages 
- Pas besoin de l'instruction atomique (couteuse)
#### Inconvénients
- Ne peut pas bénéficier de ```break``` qui économise plusieurs itérations <i>(Remarque : l'utilisation d'un flag boolean n'est pas efficace)</i>
- Génération répétée d'équipes de threads

### histogram_omp_collapse