import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;
import java.util.concurrent.TimeUnit;

import graph_element.Vertex;
import org.jgrapht.Graph;

public class Parallel implements Runnable {
    private Thread t;
    private String threadName;
    private static PrintWriter out=null;

    private static String separator=";";

    public void run() {
     //   System.out.println(threadName + " id: " + t.getId());
      //  System.out.println("starting the execution of the B&B");
        int amount_RunTime_S=0;
        Exact_GED_threads exact_GED = new Exact_GED_threads(amount_RunTime_S);
        long startTime = System.nanoTime();

        double editDistance = exact_GED.computeGED(Main.g1,Main.g2);
         long endTime = System.nanoTime();
         long elapsedTime = endTime - startTime;
    //   System.out.println(threadName+":The end of the execution of the B&B"+ "  eval:"+editDistance + "  time (s):" + TimeUnit.NANOSECONDS.toSeconds(elapsedTime)+ "  time (Ms):" +TimeUnit.NANOSECONDS.toMillis(elapsedTime)+"  nb_explored:"+ exact_GED.nb_all_path_added_to_open );


        // ---------------------------------------------------------------------------------------
        // ---------------------------------------------------------------------------------------

        /// String output= "test__"+new File(file_g1).getName()+"__"+new File(file_g2).getName();

       /* try {
            File file = new File(pathname_result_output_file);

            if(file.getParentFile()!=null){
                file.getParentFile().mkdirs();
            }

            out = new PrintWriter(new FileWriter(file, true), true);
*/

         if(editDistance==Main.upper_bound.get()) {
             synchronized(Main.fin){
                 Main.Final_results = threadName + ":" + Main.file_g1 + separator + Main.file_g2 + separator + editDistance + separator + TimeUnit.NANOSECONDS.toSeconds(elapsedTime) + separator + TimeUnit.NANOSECONDS.toMillis(elapsedTime) + separator + exact_GED.nb_all_path_added_to_open +"; all_explored nodes:"+Main.global_visited_nodes+ separator + (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) + separator + exact_GED.optimal_Path;
//                 System.out.println("Notify for main to finish..");
                     //  for(int i=0;i<NB_thread;i++){
                     Main.fin.notify(); //System.out.println("i:"+i);}

                // System.out.println("the end of threads execution");
             }

          //   System.out.println(threadName + ":" + Main.file_g1 + separator + Main.file_g2 + separator + editDistance + separator + TimeUnit.NANOSECONDS.toSeconds(elapsedTime) + separator + TimeUnit.NANOSECONDS.toMillis(elapsedTime) + separator + exact_GED.nb_all_path_added_to_open + separator + (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) + separator + exact_GED.optimal_Path);
           //  Main.Global_optimal_Path = exact_GED.optimal_Path;
                }
        /*} catch (IOException e) {
            e.printStackTrace();
        }finally {
            if(out!=null)
               out.close();
        }
    */


    }

    public void Parallel(String name) {
        threadName = name;
       // System.out.println("Creating " + threadName);
    }

    public void start() {
      //  System.out.println("Starting " + threadName);
        if (t == null) {
            t = new Thread(this, threadName);
            t.start();
        }
    }
}

/*
**/
/* */