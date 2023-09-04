
import random
import streamlit as st


def make_one(N):
    s=[]
    for i in range(0,N):
        s.append(random.randint(0,N-1) )
    return s

def initialization(N,num_pop):
    pop=[]
    for i in range(0,num_pop):
        pop.append(make_one(N))

    return pop

def get_fitness(s):
    fit=0
    for i in range(0,len(s)):
        for j in range(0,len(s)):
            if j!=i:
                if s[i]==s[j]:
                    fit+=1
                else:
                    g=float(s[i]-s[j])/float(i-j)
                    if abs(g)==1.0:
                        fit+=1

    return fit

def get_pop_fitness(population):
    pop_fitness=[]
    for s in population:
        pop_fitness.append(get_fitness(s))
    return pop_fitness

def selection(population,pop_fitness):
    
    i1=random.randint(0,len(population)-1)
    i2=random.randint(0,len(population)-1)
    while i2==i1:
        i2=random.randint(0,len(population)-1)    
    if pop_fitness[i1]<=pop_fitness[i2]:
        i=i1
    else:
        i=i2

    i3=random.randint(0,len(population)-1)
    while i3==i:
        i3=random.randint(0,len(population)-1) 
    i4=random.randint(0,len(population)-1)
    while i4==i or i4==i3:
        i4=random.randint(0,len(population)-1) 
    if pop_fitness[i3]<=pop_fitness[i4]:
        j=i3
    else:
        j=i4

    return population[i],population[j]

def crossover(s1,s2):
    p=random.randint(0,len(s1)-1)
    s=s1[0:p]
    s.extend(s2[p:])

    return s

def get_next_generation(pop,pop_fitness):
    next_gen=[]
    while len(next_gen)<len(pop):
        s1,s2=selection(pop,pop_fitness)
        s=crossover(s1,s2)
        next_gen.append(s)

    return next_gen

def mutation(population,mutate_prob):
    for i in range(0,len(population)):
        for j in range(0,len(population[i])):
            p=random.random()
            if p<=mutate_prob:
                population[i][j]=random.randint(0,len(population[i])-1)
    return population

def print_board(s):
    line=['#']*((len(s)*2)+1)
    print(''.join(line))
    
    for i in range(0,len(s)):
        line=['#']
        for j in range(0,len(s)):
            if s[j]==i:
                line.append('Q')
            else:
                line.append(' ')
            line.append('#')
        print(''.join(line))
        
        line=['#']*((len(s)*2)+1)
        print(''.join(line))

def get_board_text(s):
    lines=[]
    
    #line=['-']*((len(s)*2)+1)
    #lines.extend(line)
    #lines.append('\n')


    for i in range(0,len(s)):
        line=['|']
        for j in range(0,len(s)):
            if s[j]==i:
                line.append('Q')
            else:
                line.append(' ')
            line.append('|')
        lines.extend(line)
        lines.append('\n')
    
        #line=['-']*((len(s)*2)+1)
        #lines.extend(line)
        #lines.append('\n')

    return ''.join(lines)

def one_run(N,num_pop,num_iter,mutate_prob):   
    population=initialization(N,num_pop)
    pop_fitness=get_pop_fitness(population)

    count=0
    step_fitness_list=[]
    final_board=[]
    for i in range(0,num_iter):
        count+=1
        next_generation=get_next_generation(population,pop_fitness)
        population=mutation(next_generation,mutate_prob)
        pop_fitness=get_pop_fitness(population)
        min_fitness=min(pop_fitness)
        step_fitness_list.append(min_fitness)
        #print(i,' ',min_fitness)
        if min_fitness==0:
            print('done ',i,' ',min_fitness)
            for j in range(0,len(pop_fitness) ):
                if pop_fitness[j]==min_fitness:
                    print(population[j])
                    final_board=population[j]
                    print_board(population[j])
                    break
            break
            
    print('final count=',count,' min_fitness=',min_fitness)

    return count,min_fitness,step_fitness_list,final_board
    
N=8
num_pop=100
num_iter=500
mutate_prob=0.05

st.session_state['count']=0
st.session_state['min_fitness']=0
st.session_state['step_fitness_list']=[]
st.session_state['final_board']=[]


N=st.number_input('N Size of board', min_value=2, max_value=50, value=N)
num_pop=st.number_input('Size of population', min_value=50, max_value=10000, value=num_pop)
num_iter=st.number_input('Maximum number of iterations', min_value=2, max_value=10000, value=num_iter)
mutate_prob=st.number_input('Mutation probability', min_value=0.0, max_value=1.0, value=mutate_prob)

if st.button('Run'):
    st.session_state['count'],st.session_state['min_fitness'],st.session_state['step_fitness_list'],st.session_state['final_board']=one_run(N,num_pop,num_iter,mutate_prob)

st.text('count='+str(st.session_state['count']))
st.text('minimum fitness='+str(st.session_state['min_fitness']))
st.line_chart(st.session_state['step_fitness_list'])

board_text=get_board_text(st.session_state['final_board'])
st.text(board_text)
