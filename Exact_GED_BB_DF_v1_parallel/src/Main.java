import graph_element.Edge;
import graph_element.Vertex;
import imoprt_exoprt_jgrapht_gxl.Import_JGraphT_From_GXL;
import imoprt_exoprt_jgrapht_gxl.Import_TUDataset_from_gxl;
import org.jgrapht.UndirectedGraph;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Stack;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Created by user on 27/03/2017.
 */
public class Main {

    private static int cost_node_sub=0;
    private static int cost_node_del_ins=0;

    private static int cost_edge_sub=0;
    private static int cost_edge_del_ins=0;

    public static String file_g1=null;
    public static String file_g2=null;

    private static PrintWriter out=null;

    private static String separator=";";

    private static int NB_thread=30;

   public static UndirectedGraph<Vertex, Edge> g1=null;
   public static UndirectedGraph<Vertex, Edge> g2=null;
   //public static int UB =10000;
   public static Stack<Path> path_Stack;
   public  static Path Global_optimal_Path;
   public static int global_visited_nodes=0;
   public static String Final_results="";
   public static AtomicInteger upper_bound = new AtomicInteger(1000);
    public static CyclicBarrier barrier;
   public  static String pathname_result_output_file=null;
   public static Parallel fin=new Parallel();

   public static int amount_RunTime_S = 0;

   public static void main(String[] args) { path_Stack=new Stack<Path>();


     String test_benchmark=null; // CMU, MUTA, GREC, PATH (acyclic, alkane, pah, mao)

        upper_bound.set(1000);
        if(args.length>=10)
        {
            try {
                cost_node_sub = Integer.parseInt(args[0]);
                cost_node_del_ins = Integer.parseInt(args[1]);
                cost_edge_sub = Integer.parseInt(args[2]);
                cost_edge_del_ins = Integer.parseInt(args[3]);

                file_g1 = args[4];
                file_g2 = args[5];

                pathname_result_output_file=args[6];

                test_benchmark=args[7];

                amount_RunTime_S = Integer.parseInt(args[8]);

                NB_thread = Integer.parseInt(args[9]);

            }catch (NumberFormatException e){
                System.err.println("Argument : " + e.getMessage() + " must be an integer.");
                System.exit(1);
            }
        }


        if(test_benchmark.equals("PATH")) {
            Main.g1 = Import_JGraphT_From_GXL.import_simple_graph(file_g1);
            g2 = Import_JGraphT_From_GXL.import_simple_graph(file_g2);
        }
        else if(test_benchmark.equals("GREC")) {
            g1 = Import_JGraphT_From_GXL.import_simple_graph_from_GREC_GED(file_g1);
            g2 = Import_JGraphT_From_GXL.import_simple_graph_from_GREC_GED(file_g2);
        }
        else if(test_benchmark.equals("MUTA")) {
            g1 = Import_JGraphT_From_GXL.import_simple_graph_from_MUTA_GED(file_g1);
            g2 = Import_JGraphT_From_GXL.import_simple_graph_from_MUTA_GED(file_g2);
        }
        else if(test_benchmark.equals("CMU")) {
            g1 = Import_JGraphT_From_GXL.import_simple_graph_from_CMU_GED(file_g1);
            g2 = Import_JGraphT_From_GXL.import_simple_graph_from_CMU_GED(file_g2);
        }else if (test_benchmark.equals("TUDataset")) {
            g1 = Import_TUDataset_from_gxl.import_simple_graph_label_only(file_g1);
            g2 = Import_TUDataset_from_gxl.import_simple_graph_label_only(file_g2);
        }


        if(g1==null)
        {
            System.out.println("Can't Load the First Graph : "+file_g1);
            return;
        }
        if(g2==null)
        {
            System.out.println("Can't Load the Second Graph : "+file_g2);
            return;
        }

       barrier = new CyclicBarrier(NB_thread);
        //Exact_GED_AStar exact_GED = new Exact_GED_AStar();
        Exact_GED_BB_DF exact_GED = new Exact_GED_BB_DF(amount_RunTime_S);

        GED_Operations_Cost.setAll_Operations_cost(cost_node_sub,cost_node_del_ins,cost_node_del_ins,cost_edge_sub,cost_edge_del_ins,cost_edge_del_ins,1);

        GED_Operations_Cost.setIs_Weight(true);
        //GED_Operations_Cost.setIs_Label(true);

        // ---------------------------------------------------------------------------------------
        // ---------------------------------------------------------------------------------------
      /*  Parallel T1 = new Parallel();
        T1.Parallel("thread-1");
        T1.start();
        Parallel T2 = new Parallel();
        T2.Parallel("thread-2");
        T2.start();
        Parallel T3 = new Parallel();
        T3.Parallel("thread-3");
        T3.start();*/
       Parallel[] T1 = new Parallel[50];
      long startTime = System.nanoTime();

        for(int i=1;i<NB_thread+1;i++)
        {
            T1[i] = new Parallel();
           T1[i].Parallel("thread-"+i);
           T1[i].start();
                   }
       synchronized(fin){
           try{
               System.out.println("Waiting for threads to finish...NB_threads"+NB_thread);
          //  for(int i=0;i<NB_thread;i++){
                fin.wait(); //System.out.println("i:"+i);}
           }catch(InterruptedException e){
               e.printStackTrace();
           }
         //  System.out.println("the end of threads execution");
       }

       try {
           TimeUnit.SECONDS.sleep(5);
       } catch (InterruptedException e) {
           e.printStackTrace();
       }
       double editDistance = Main.upper_bound.doubleValue();//exact_GED.computeGED(g1,g2);

        long endTime = System.nanoTime();

        long elapsedTime = endTime - startTime;

      //  System.out.println("cbon ça marche");

        // ---------------------------------------------------------------------------------------
        // ---------------------------------------------------------------------------------------

        /// String output= "test__"+new File(file_g1).getName()+"__"+new File(file_g2).getName();

        try {
            File file = new File(pathname_result_output_file);

            if(file.getParentFile()!=null){
                file.getParentFile().mkdirs();
            }

            out = new PrintWriter(new FileWriter(file, true), true);
            out.println("Final_results:"+Final_results);
       //     System.out.println(Final_results);
         //   out.println(file_g1+separator+file_g2+separator + editDistance + separator + TimeUnit.NANOSECONDS.toSeconds(elapsedTime)+separator +"time (MS):"+TimeUnit.NANOSECONDS.toMillis(elapsedTime) + separator + exact_GED.nb_all_path_added_to_open + separator + (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) + separator + exact_GED.optimal_Path );

        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            if(out!=null)
                out.close();
        }
        /*
        System.out.println(exact_GED.optimal_Path.toString());
        System.out.println(editDistance);
        System.out.println("\n nb_all_path_added_to_open = "+exact_GED.nb_all_path_added_to_open);
        System.out.println("---------------------------------------- time : ");
        System.out.println("Total execution time: " +elapsedTime +" Nanos");
        System.out.println("Total execution time: " +TimeUnit.NANOSECONDS.toMicros(elapsedTime)+" Micros");
        System.out.println("Total execution time: " +TimeUnit.NANOSECONDS.toMillis(elapsedTime)+" Millis");
        */
        /*
        System.out.println("Total execution time: " +
                String.format("%d min, %d sec",
                        TimeUnit.NANOSECONDS.toHours(elapsedTime),
                        TimeUnit.NANOSECONDS.toSeconds(elapsedTime) -
                                TimeUnit.MINUTES.toSeconds(TimeUnit.NANOSECONDS.toMinutes(elapsedTime))));
                                */


    }
}
