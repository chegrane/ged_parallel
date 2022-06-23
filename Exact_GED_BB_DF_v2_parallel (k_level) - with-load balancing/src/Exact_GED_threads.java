import java.util.concurrent.CyclicBarrier;
import graph_element.Vertex;
import org.jgrapht.Graph;

import java.util.ArrayList;
import java.util.List;
import java.util.Stack;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.Callable;
import java.util.concurrent.CyclicBarrier;

public class Exact_GED_threads {
// Exact Graph Edit Distance (GED) with Branch and Bound (BB) Depth First stratigy (DF)
        /**
         * The set OPEN of partial edit paths contains the search tree nodes
         * to be processed in the next steps.
         */
     //   private Stack<Path> path_Stack;
         /* In the branch and Bound Depth first we use stack to manage the backtraking in the search tree,
	 									when we complete to process an intermediate node, we back to it's father.*/
        private double upper_bound = Double.MAX_VALUE;
        private long amount_RunTime=0;
    private  CyclicBarrier barrier1;
  private   Stack<Path> path_Stack1;
    private   Stack<Path> p_Stack;
        // Just for debugging purpose
        Path optimal_Path;
        int nb_all_path_added_to_open=0; // just for debugging
        /**
         * Default Constructor
         */
        public Exact_GED_threads()
        {
     //       path_Stack=new Stack<Path>();
        }

        public Exact_GED_threads(long amount_RunTime) {

            path_Stack1=new Stack<Path>();
            p_Stack=new Stack<Path>();
            this.amount_RunTime = amount_RunTime;
        }

        /**
         * Compute the exact edit distance between two graphs.
         * The method implements A* algorithm
         * @param g1 from graph
         * @param g2 to graph
         * @return returns the exact edit distance between the to graphs
         */
        @SuppressWarnings({ "rawtypes", "unchecked" })
        public double computeGED(Graph g1, Graph g2)
        { barrier1=Main.barrier;
            // if both graph are empty, then the edit distance is "0"
            if (g1.vertexSet().size() == 0 && g2.vertexSet().size() == 0) {
                return 0;
            }

            // if the graph g1 is empty (g2 is not), then
            // edit distance is = the cost of (insertion of all vertices of g2) + (insertion of all edges of g2)

            if (g1.vertexSet().size() == 0) {
                return (GED_Operations_Cost.getVertex_insertion_cost() * g2.vertexSet().size() + GED_Operations_Cost.getEdge_insertion_cost() * g2.edgeSet().size());
            }

            // if the graph g1 have vertices and edges; and g2 is empty, then
            // edit distance is = the cost of (deletion of all vertices of g1) + (deletion of all edges of g1)

            if (g2.vertexSet().size() == 0) {
                return (GED_Operations_Cost.getVertex_deletion_cost() * g1.vertexSet().size() + GED_Operations_Cost.getEdge_deletion_cost() * g1.edgeSet().size());
            }
         //   upper_bound = Main.UB;//h_function.compute(g1,g2,"max");

            // local varibal, listV1: set of vertices of g1 ; listV2: set of vertices of g2
            ArrayList<Vertex> listV1 = new ArrayList<>(g1.vertexSet());
            ArrayList<Vertex> listV2 = new ArrayList<>(g2.vertexSet());

          //  System.out.println("name+++--thread"+Thread.currentThread().getName());
            // ---------------------- step 1 : Prepare initial paths (first level of the search tree)
if(Thread.currentThread().getName().equalsIgnoreCase("thread-1")) {
    // substitution
    Main.upper_bound.set((int)h_function.compute(g1,g2,"max"));
   for (Vertex w : listV2) {
        Edit_Operation vertex_substitution_operation = new Edit_Operation(listV1.get(0), w);
        Path path = new Path(g1, g2);
        path.add(vertex_substitution_operation);
        // Insert substitution (u1 --> w) into OPEN
        if (path.getG_cost_PLUS_h_cost() < Main.upper_bound.doubleValue()) {
           // Main.path_Stack.push(path);
            Main.path_Stack.add(path);

            //OPEN.add(path);
            nb_all_path_added_to_open++;
        }
    }

    // deletion
    Edit_Operation vertex_deletion_operation = new Edit_Operation(listV1.get(0), null);
    Path path0 = new Path(g1, g2);
    path0.add(vertex_deletion_operation);
    // Insert deletion (u1 --> null) into OPEN

    if (path0.getG_cost_PLUS_h_cost() < Main.upper_bound.doubleValue()) {
       // Main.path_Stack.push(path0);
        Main.path_Stack.add(path0);

        nb_all_path_added_to_open++;
    }
}//else{ while(Main.path_Stack.empty()){} }
            Path pMin;
            // add threads
            //while(true)
//System.out.println("UBmain:"+Main.upper_bound);
            try {
                               barrier1.await();

         //       System.out.println("Barrière dépassée : Le thread ");
            } catch (InterruptedException | BrokenBarrierException e) {
                e.printStackTrace();
            }

            int size=Main.path_Stack.size();
            size= (int) size/Main.NB_thread;

            /*/try {
                barrier1.await();

                       } catch (InterruptedException | BrokenBarrierException e) {
                e.printStackTrace();
            }*/
            size++;
int iteration=0;
                //section critique
            int se=0;
          //for(int i=0;i<size;i++)
            while(se<size)
                    {synchronized(Main.path_Stack) {
                if(Main.path_Stack.size()>0){Path p1 = Main.path_Stack.remove()/*pop()*/; path_Stack1.push(p1);
                se++;
          }
            }
            }
           // System.out.println("c bon size:"+size);
            while(!Main.path_Stack.isEmpty()||!path_Stack1.empty()) // a loop to process all the vertices in g1, wa treat all the sub-tree.
            {
                // Return pMin and delete all argmin_p{g(p)+h(p)} paths
                // get the node pMin from OPEN, this depend on the strategy implemented.
                pMin = argMin();
                // System.out.println(pMin.toString());
                if (pMin!=null) {
                if (pMin.isCompleteEditPath()) {
                 /*   if(optimal_Path==null)
                    {
                        optimal_Path = new Path(pMin); // Make a copy for debugging purpose

                        Main.upper_bound.set(((int)pMin.getG_cost()));
                    }
                    else*/
                    {
                        if (pMin.getG_cost() < Main.upper_bound.get())//optimal_Path.getG_cost())
                        {   optimal_Path = new Path(pMin); // Make a copy for debugging purpose
                            Main.upper_bound.set((int) pMin.getG_cost());
                       //     System.out.println("UB main:" +Main.upper_bound.get());
                        }
                    }


                    /// System.out.println(optimal_Path.toString());
                    /// System.out.println("G_cost = "+optimal_Path.getG_cost()+" | g+h = "+optimal_Path.getG_cost_PLUS_h_cost()+" | upper_bound = "+upper_bound);
                } else {
                    /// Let min_path = {u_1 --> v_i1,...,u_k --> v_ik}
                    List<Vertex> remainsV2 = pMin.getRemaining_unprocessed_vertex_g2();
                    int index_processed_vertices_g1 = pMin.getIndex_processed_vertices_g1();

                    if (index_processed_vertices_g1 < listV1.size()) {
                        // substitution
                        for (Vertex w1 : remainsV2) {
                            Path newP1 = new Path(pMin);
                            Edit_Operation newOp1 = new Edit_Operation(listV1.get(index_processed_vertices_g1), w1);
                            newP1.add(newOp1);
                            // Add substitution to pMin, then add the new path to OPEN

                            /// System.out.println("---------- Midele node : g+h = "+newP1.getG_cost_PLUS_h_cost());

                            if (newP1.getG_cost_PLUS_h_cost() < Main.upper_bound.doubleValue()) {
                                //       Main.path_Stack.push(newP1);
                                add_Path(newP1);
                                nb_all_path_added_to_open++;
                            }
                        }
                        // deletion
                        Path newP2 = new Path(pMin);
                        Edit_Operation newOp2 = new Edit_Operation(listV1.get(index_processed_vertices_g1), null);
                        newP2.add(newOp2);
                        // Add deletion to pMin, then add the new path to OPEN

                        /// System.out.println("---------- Midele node : g+h = "+newP2.getG_cost_PLUS_h_cost());

                        if (newP2.getG_cost_PLUS_h_cost() < Main.upper_bound.doubleValue()) {
                            //  Main.path_Stack.push(newP2);
                            add_Path(newP2);
                            nb_all_path_added_to_open++;
                        }
                    } else {
                        Path newP3 = new Path(pMin);
                        for (Vertex w2 : remainsV2) {
                            Edit_Operation newOp3 = new Edit_Operation(null, w2);
                            newP3.add(newOp3);
                        }
                        // Add insertion to pMin, then add the new path to OPEN

                        /// System.out.println("---------- Midele node : g+h = "+newP3.getG_cost_PLUS_h_cost());

                        if (newP3.getG_cost_PLUS_h_cost() < Main.upper_bound.doubleValue()) {
                            // Main.path_Stack.push(newP3);
                            add_Path(newP3);
                            nb_all_path_added_to_open++;
                        }
                    }
                }
if(iteration<5){  synchronized (Main.path_Stack) {Main.path_Stack.addAll( path_Stack1);} path_Stack1.clear();}
                    else if(iteration>100 && Thread.currentThread().getName().equalsIgnoreCase("thread-1")==true){

                    Main.path_Stack_load.addAll(Main.path_Stack); Main.path_Stack.clear();
}

                if (iteration % Main.k_level == 0) {
                    int zi = (int) (path_Stack1.size() / 5);
                    if (zi > 0) { //System.out.println(zi);
                        //               for(int i=0;i<zi;i++)p_Stack.push(path_Stack1.remove(0));
                        synchronized (Main.path_Stack) {
                            Main.path_Stack.addAll(path_Stack1);
                            }
                            path_Stack1.clear(); //path_Stack1.clear();
                            //for(int i=0;i<zi;i++)path_Stack1.push(p_Stack.pop());

                    }
                }
            }
            }

            Main.global_visited_nodes=Main.global_visited_nodes+nb_all_path_added_to_open;
            try {
                barrier1.await();
                //  System.out.println("Barrière dépassée fin : Le thread ");
            } catch (InterruptedException | BrokenBarrierException e) {
                e.printStackTrace();
            }
            if(optimal_Path==null){return -1;} else return optimal_Path.getG_cost();
//            // optimal_Path.getG_cost();
         //  if(optimal_Path==null){return 0;} else return optimal_Path.getG_cost();
        }
        /**
         * Get pMin and delete all argmin_p{g(p)+h(p)} paths
         *
         * @return returns the path p with the minimum g(p)+h(p)
         */
        private Path argMin()
        { Path p=null;
            //Path p = OPEN.poll();
            if(path_Stack1.size()>0){p = path_Stack1.pop();}
                else  if(Main.path_Stack_load.size()>0){
                synchronized(Main.path_Stack_load) {
                    if(Main.path_Stack_load.size()>0)
                        p = Main.path_Stack_load.pop();}

            }
            else {//if(Main.path_Stack.size()>5||Thread.currentThread().getName().equalsIgnoreCase("thread-1")==true) {
                synchronized(Main.path_Stack) {
                    if(Main.path_Stack.size()>0)
                        p = Main.path_Stack.remove();}}

            //while(p.getG_cost_PLUS_h_cost() == OPEN.peek().getG_cost_PLUS_h_cost()) // Double comparison !!! To be fixed!
            //	OPEN.poll();

            return p;
        }

    private void add_Path(Path p)
    {
        //Path p = OPEN.poll();
//if(nb_all_path_added_to_open>1000)
    if(Main.path_Stack_load.size()<5){ /*Main.path_Stack.push(p);}//*/
  if(path_Stack1.size()>1) {   Main.path_Stack_load.push(path_Stack1.get(0)); path_Stack1.remove(0);}
                            }

    {path_Stack1.push(p);}
    //else{
      // if(this.nb_all_path_added_to_open>0)
        //      else
        //while(p.getG_cost_PLUS_h_cost() == OPEN.peek().getG_cost_PLUS_h_cost()) // Double comparison !!! To be fixed!
        //	OPEN.poll();
    //}
    }
}
