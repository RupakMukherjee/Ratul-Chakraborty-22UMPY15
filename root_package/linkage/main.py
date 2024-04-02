#REQUIRED LIBRARIES AND SYMBOLS
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time
import numpy as np
import sympy as sp
t,u,v=sp.symbols('t u v')






def Linkage(list):
  
  def LINKING_NUMBER(points1,points2):
    
    # Convert points to numpy array for easier manipulation
    points1 = np.array(points1)
    points2 = np.array(points2)

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the points
    ax.scatter(points1[:, 0], points1[:, 1], points1[:, 2], color='red', marker='o')
    ax.scatter(points2[:, 0], points2[:, 1], points2[:, 2], color='blue', marker='o')

    # Connect points with vectors forming a loop
    for i in range(len(points1) - 1):
        vector1 = points1[i + 1] - points1[i]
        ax.quiver(points1[i, 0], points1[i, 1], points1[i, 2], vector1[0], vector1[1], vector1[2],
                  color='blue', arrow_length_ratio=0.1)

        # Connect starting and ending points in the same orientation
        ax.plot([points1[i, 0], points1[i + 1, 0]], [points1[i, 1], points1[i + 1, 1]],
                [points1[i, 2], points1[i + 1, 2]], color='blue')
        
    for i in range(len(points2) - 1):
        vector2 = points2[i + 1] - points2[i]
        ax.quiver(points2[i, 0], points2[i, 1], points2[i, 2], vector2[0], vector2[1], vector2[2],
                  color='red', arrow_length_ratio=0.1)

        # Connect starting and ending points in the same orientation
        ax.plot([points2[i, 0], points2[i + 1, 0]], [points2[i, 1], points2[i + 1, 1]],
                [points2[i, 2], points2[i + 1, 2]], color='red')    

    # Connect the last point to the first point to form a loop
    last_vector1 = points1[0] - points1[-1]
    ax.quiver(points1[-1, 0], points1[-1, 1], points1[-1, 2], last_vector1[0], last_vector1[1], last_vector1[2],
              color='blue', arrow_length_ratio=0.1)
    ax.plot([points1[-1, 0], points1[0, 0]], [points1[-1, 1], points1[0, 1]],
            [points1[-1, 2], points1[0, 2]], color='blue')
    
    last_vector2 = points2[0] - points2[-1]
    ax.quiver(points2[-1, 0], points2[-1, 1], points2[-1, 2], last_vector2[0], last_vector2[1], last_vector2[2],
              color='red', arrow_length_ratio=0.1)
    ax.plot([points2[-1, 0], points2[0, 0]], [points2[-1, 1], points2[0, 1]],
            [points2[-1, 2], points2[0, 2]], color='red')


   # Triangualtion
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
                 if (0<=angle<90) or (270<angle<=360):
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
    
    # Set axis limits
    ax.set_xlim([min(points1[:, 0]) - 1, max(points1[:, 0]) + 1])
    ax.set_ylim([min(points1[:, 1]) - 1, max(points1[:, 1]) + 1])
    ax.set_zlim([min(points1[:, 2]) - 1, max(points1[:, 2]) + 1])
    ax.set_xlim([min(points2[:, 0]) - 1, max(points2[:, 0]) + 1])
    ax.set_ylim([min(points2[:, 1]) - 1, max(points2[:, 1]) + 1])
    ax.set_zlim([min(points2[:, 2]) - 1, max(points2[:, 2]) + 1])
    ax.add_collection3d(loop)
    #VISUALISING THE LINKS
    plt.show()
  LINK=[]
  for lnk in list:
    points1=lnk[0]
    points2=lnk[1]
    LINK.append(LINKING_NUMBER(points1,points2))
    
  if LINK[0]==LINK[1]:
      print("THE GIVEN LINKS ARE  SAME.")
      if LINK[0]==LINK[1]==1:
        print("IN BOTH OF THE LINKS, THE LOOPS ARE KNOTTED IN A SINGLE LINK, AND SO ARE HOPF LINKS.")
      elif LINK[0]==LINK[1]==0:
        print("IN BOTH OF THE LINKS, THE LOOPS ARE SEPERATE, AND SO ARE UNLINKS.")  
  elif LINK[0]!=LINK[1]:
      print('THE GIVEN LINKS ARE DIFFERENT.')

