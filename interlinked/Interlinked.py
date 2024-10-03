#Follow the instructions given in the README.md file to run this script.

#Requisites
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time
import math
import numpy as np
import sympy as sp
from itertools import combinations
t,u,v=sp.symbols('t u v')
start_time=time.time()


def Plot(data):
   
    #Create a 3D plot
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  for dataset in data: 
    # Extract points from the dataset
     points = np.array(dataset)
    
    #Plot the points
     ax.scatter(points[:, 0], points[:, 1], points[:, 2],  marker='o')

    #Connect points with vectors forming a loop
     for i in range(len(points) - 1):
        vector = points[i + 1] - points[i]
        ax.quiver(points[i, 0], points[i, 1], points[i, 2], vector[0], vector[1], vector[2],
                   arrow_length_ratio=0.1)
        ax.plot([points[i, 0], points[i + 1, 0]], [points[i, 1], points[i + 1, 1]],
                [points[i, 2], points[i + 1, 2]])

    #Connect the last point to the first point to form a loop
     last_vector = points[0] - points[-1]
     ax.quiver(points[-1, 0], points[-1, 1], points[-1, 2], last_vector[0], last_vector[1], last_vector[2],
               arrow_length_ratio=0.1)
     ax.plot([points[-1, 0], points[0, 0]], [points[-1, 1], points[0, 1]],
            [points[-1, 2], points[0, 2]])

    #Calculate axis limits based on the points
     min_x, max_x = points[:, 0].min(), points[:, 0].max()
     min_y, max_y = points[:, 1].min(), points[:, 1].max()
     min_z, max_z = points[:, 2].min(), points[:, 2].max()

    #Increase margins slightly
     margin = 10.0
     ax.set_xlim([min_x - margin, max_x + margin])
     ax.set_ylim([min_y - margin, max_y + margin])
     ax.set_zlim([min_z - margin, max_z + margin])
    
  plt.show()


def LINKING_NUMBER(dataset):
    points1=dataset[0]
    points2=dataset[1]
    #Convert points to numpy array for easier manipulation
    points1 = np.array(points1)
    points2 = np.array(points2)

    
    

   #Triangualtion
    triangles = []
    for i in range(1, len(points1)-1):
        triangle = points1[0], points1[i], points1[i+1]
        triangles.append(triangle)
    
    
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
              
              #Orientation
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

#Register your data 

Time_stamp=[[( -9 , 0 , 0 ),( -8 , 0 , 0 ),( -6 , 0 , 2 ),( -6 , 2 , 0 ),( -6 , 3 , 1 ),( -9 , 3 , 2 ),( -8 , 3 , 1 )],[( 0 , 4 , 0 ),( 4 , 0 , 0 ),( 2.5 , -3 , 3 ),( 2.5 , -3 , 9 ),( -2 , -2 , 8 ),( -6 , 1 , 4 ),( -8 , 1.5 , 0 ),( -6 , 0 , -4 )],[( 0 , 0 , 0 ),( 1.5 , -1 , 0 ),( 1.5 , -1 , 3 ),( 0.5 , -0.5 , 14 ),( -4 , 0 , 3 ),( 2 , 5 , 2 )]]


#Plotting the data

Plot(Time_stamp_5)


#Generating different combination of loops

def Identify_links(data):
    combinations_two_lists = [list(combination) for combination in combinations(data, 2)]
    
    Hopf_link=[]
    for combination in combinations_two_lists:
       
       linking_number = LINKING_NUMBER(combination)
       if linking_number==1:
          Hopf_link.append(1)
    print("The number of links identified are ", len(Hopf_link))        

#Call Identify_links
Identify_links(Time_stamp)
end_time=time.time()
print(end_time-start_time)
