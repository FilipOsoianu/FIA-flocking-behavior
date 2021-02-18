    def apply_behaviour(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)        
        separation = self.separation(boids)

  

        self.acc =sum( self.acc, alignment)       
        self.acc =sum( self.acc, cohesion)        
        self.acc =sum( self.acc, separation)
        
    def updateRock(self):
        self.pos = sum(self.pos, self.vel)            
        self.vel = sum(self.vel, self.acc)
        if norm(self.vel) > self.max_speed:
            self.vel = mul(div(self.vel, norm(self.vel)), self.max_speed)
        self.acc = [0,0]
            # return True if the sprite is old and needs to be destroyed
        if self.age < self.lifespan: 
            return False
        else:
            return True

    
    def collide(self, other_object):
        """
        Method that takes as imput a sprite and another object (e.g. the ship, a sprite)
        and returns True if they collide, else False
        """
        distance = dist(self.pos, other_object.get_pos())
        sum_radii = self.radius + other_object.get_radius()
        
        if distance < sum_radii:
            return True
        else:
            return False
        
    
    def align(self, boids):
        
        steering = [0,0]
        total = 0
        avg_vector = [0,0]
        for boid in boids:
            if norm(sub(boid.pos, self.pos)) < self.perception:
                avg_vector = sum(avg_vector,boid.vel)
                total += 1
        if total > 0:
            avg_vector = div(avg_vector,total)
            avg_vector = mul(div(avg_vector, norm(avg_vector)), self.max_speed)
            steering = sub(avg_vector,self.vel)

        return steering
    
    
    def cohesion(self, boids):
        
        steering = [0,0]
        total = 0
        center_of_mass = [0,0]
        for boid in boids:
            if norm(sub(boid.pos, self.pos)) < self.perception:
                center_of_mass += boid.pos
                total += 1
        if total > 0:
            center_of_mass = div(center_of_mass, total)
            vec_to_com = sub(center_of_mass, self.pos)
            if norm(vec_to_com) > 0:
                vec_to_com = mul(div(vec_to_com, norm(vec_to_com)), self.max_speed)
            steering = sub(vec_to_com ,self.vel)
            if norm(steering)> self.max_force:
                steering = mul(div(steering ,norm(steering)), self.max_force)
        
       
        return steering
    
    def separation(self, boids):
        steering = [0,0]
        total = 0
        avg_vector = [0,0]
        for boid in boids:
            distance = norm(sub(boid.pos, self.pos))
            if self.pos != boid.pos and distance < self.perception:
                diff = sub(self.pos, boid.pos)
                diff =div(diff, distance)
                avg_vector = sum(avg_vector,diff)
                total += 1
        if total > 0:
            avg_vector = div(avg_vector, total)
            if norm(steering) > 0:
                avg_vector = mul(div(avg_vector, norm(steering)), self.max_speed)
            steering =sub( avg_vector , self.vel)
            if norm(steering) > self.max_force:
                steering = mul(div(steering, norm(steering)), self.max_force)


        return steering
    
    def edges(self):
        if self.pos[0] > CANVAS_RES[0]:
            self.pos[0] = 0
        elif self.pos[0] < 0:
           self.pos[0] =  CANVAS_RES[0]
        if self.pos[1] >  CANVAS_RES[1]:
            self.pos[1] = 0
        elif self.pos[1] < 0:
            self.pos[1] =  CANVAS_RES[1]

        

def norm(self):
    p=2
    sum = 0
    for x in self:
        sum += x**p
        
    return sum**(1/p)

def sub(self, other):

     return [x1 - x2 for (x1, x2) in zip(self, other)]

def sum(self, other):

     return [x1 + x2 for (x1, x2) in zip(self, other)]

def div(self, number):
     return [x / number for x in self]
    
    
def mul(self, number):
    return [x * number for x in self]