#Follow the instructions given in the README.md file to run this script.

#Requisites
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time
from itertools import combinations
import numpy as np
import copy
import sympy as sp
t,u,v=sp.symbols('t u v')

#Helicity of n-component link (n=2,3,4,5,...........)
def n_component_Helicity(n_component_link):

    #Deep copy
    n_copy = copy.deepcopy(n_component_link)
    for i in range(len(n_copy)):
       n_copy[i].append([])
    

    #Visuals
    def Visualisation(points):

        points = np.array(points)
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], marker='o')
        for i in range(len(points) - 1):
          ax.plot([points[i, 0], points[i + 1, 0]], [points[i, 1], points[i + 1, 1]],[points[i, 2], points[i + 1, 2]])
          ax.plot([points[-1, 0], points[0, 0]], [points[-1, 1], points[0, 1]],[points[-1, 2], points[0, 2]])

    #Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #Plot each loop with a different color
    for i in range(len(n_component_link)):
       Visualisation(n_component_link[i])
    plt.show()

    #Linking Number
    def LINKING_NUMBER(points1,points2):
    
        #Convert points to numpy array for easier manipulation
        points1 = np.array(points1)
        points2 = np.array(points2)

        #Triangualtion
        triangles = []
        for i in range(1, len(points1)-1):
            triangle = points1[0], points1[i], points1[i+1]
            triangles.append(triangle)
        loop = Poly3DCollection(triangles, edgecolor='k', linewidths=1, alpha=0.5)
    
        #Equations of all the Blue Triangles and Equations of the Red Vectors
        def Line_equation(point0,point1):
           return np.array(point0)-(np.array(point1)-np.array(point0))*t
        print('THE LIST OF PARAMETRIC EQUATIONS OF THE RED VECTORS IS :')
        Red_Vectors=[]   
        for i in range(len(points2)):
          if (i<len(points2)-1):
            la=points2[i]
            lb=points2[i+1]
            Red_Vectors.append(Line_equation(la,lb))
        
          else:
            last_point=points2[i]
            first_point=points2[0]
            Red_Vectors.append(Line_equation(last_point,first_point))
        print(Red_Vectors)

        def Plane_equation(vertices0,vertices1,vertices2):
           return np.array(vertices0)+((np.array(vertices1)-np.array(vertices0))*u)+((np.array(vertices2)-np.array(vertices0))*v)
        print('THE LIST OF PARAMETRIC EQUATIONS OF THE BLUE TRIANGLES IS :')
        Blue_Triangles=[]
        for  tri in (triangles[:]):
          p0=tri[0]
          p1=tri[1]
          p2=tri[2]
          Blue_Triangles.append(Plane_equation(p0,p1,p2))
        print(Blue_Triangles)  
    
        #Solving the matrix equation for the crossing point
        Linking_List=[]
        def Solution(La,Lb,P0,P1,P2):

          A=sp.Matrix([[-(Lb[0]-La[0]),(P1[0]-P0[0]),(P2[0]-P0[0])],
                 [-(Lb[1]-La[1]),(P1[1]-P0[1]),(P2[1]-P0[1])],
                 [-(Lb[2]-La[2]),(P1[2]-P0[2]),(P2[2]-P0[2])]])
          X=sp.Matrix([t,u,v])
          B=sp.Matrix([(La[0]-P0[0]),(La[1]-P0[1]),(La[2]-P0[2])])

          Matrix_equation = sp.Eq(A * X,B)
          solution = sp.solve(Matrix_equation, (t, u, v))

          print(solution)
          if len(solution) == 0:
              print('Solution does not exist')    
      
          else:
              try:
                if 0<=solution[t]<=1 and 0<=solution[u]<=1 and 0<=solution[v]<=1 and solution[u]+solution[v]<=1:
                  print(solution)
              
                  #ORIENTATION OF THE SEIFERT SURFACE
                  def Gradient_Vector(u_value,v_value):
                     P01=P1-P0
                     P02=P2-P0
                     normal_vector=np.cross(P01,P02)
                     solution_vector=np.array(Lb)-np.array(La)
                     angle=np.degrees(np.arccos(np.dot(normal_vector,solution_vector)/(np.linalg.norm(normal_vector)*np.linalg.norm(solution_vector))))
                     print("THE ANGLE BETWEEN THE GRADIENT VECTOR AND THE SOLUTION VECTOR IS :", angle)
                     if (0<=angle<90):
                      Linking_List.append(1)
                     elif (90<angle<270):
                      Linking_List.append(-1)
                     print(Linking_List)
                  print(Gradient_Vector(solution[u],solution[v]))
                else:
                   print('Solution does not exist')
              except TypeError:
                   print("Solution does not exist") 


        for tri in (triangles[:]):
          print("For triangle :",tri)
          P0=tri[0]
          P1=tri[1]
          P2=tri[2]
          for i in range(len(points2)):
               if (i<len(points2)-1):
                   La=points2[i]
                   Lb=points2[i+1]
                   print(Solution(La,Lb,P0,P1,P2))
               else:
                   Last_point=points2[i]
                   First_point=points2[0]
                   print(Solution(Last_point,First_point,P0,P1,P2))
        Linking_Number=0
        for i in Linking_List[:]:
           Linking_Number=Linking_Number+i
        return abs(Linking_Number)

    #Necessary Condition for n-component link
    r=len(n_component_link)
    p=(r*(r-1))/2
    def f(r,p):
        return ((r-2)*p)/r - (p-r+1)
    if f(r,p)==0:
        print(f"The Structure can be a {r} component Hopf ring")    
    
    #Sufficient Condition for n-component link
    index_list=[]
    for i in range(len(n_component_link)):
        index_list.append(i)
    index_pairs=list(combinations(index_list, 2))
    n_link=[]
    for i in range(len(index_pairs)):
        ring1=n_component_link[index_pairs[i][0]]
        ring2=n_component_link[index_pairs[i][1]]
        n_link.append(LINKING_NUMBER(ring1,ring2))
        if LINKING_NUMBER(ring1,ring2)==1:
            n_copy[index_pairs[i][0]][-1].append(1)
            n_copy[index_pairs[i][1]][-1].append(1)
    for i in range(len(n_copy)):
        n_copy[i][-1][:]=[sum(n_copy[i][-1])]
    n_sort=[sublist[-1][0] for sublist in n_copy]     
    n_sort=np.sort(n_sort)  
    if all(x == 1 for x in n_sort[:-1]):
        if n_sort[-1] == sum(n_sort[:-1]):
            print(f'The Structure is a {r} component Hopf link with Helicity of {r-1}') 
    return r-1
               
#Register your date
Two_component_link=[[(1.5, 2, 0.5), (0.5, 3, 3), (3, 3, 3), (3, 3, 0.5)],[(0, 6.5, 1.5), (0, 2.5, 1.5), (1.5, 0, 1.5),(1.5, 6.5, 1.5)]]
Three_component_link=[[(1.5, 2, 0.5), (0.5, 3, 3), (3, 3, 3), (3, 3, 0.5)],[(0, 6.5, 1.5), (0, 2.5, 1.5), (1.5, 0, 1.5), (1.5, 6.5, 1.5)],[(2, 5, 0), (1, 6, 2), (4, 6, 2), (4, 6, 0)]]


#Comparison
H1=n_component_Helicity(Two_component_link)
H2=n_component_Helicity(Three_component_link)
if H1==H2:
    print("THE OBTAINED TWO STRUCTURES ARE SAME")
else:
    print("THE OBTAINED TWO STRUCTURES ARE DIFFERENT")    
