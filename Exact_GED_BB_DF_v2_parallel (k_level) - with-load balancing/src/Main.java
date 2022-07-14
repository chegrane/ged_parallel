import imoprt_exoprt_jgrapht_gxl.Import_JGraphT_From_GXL;
import imoprt_exoprt_jgrapht_gxl.Import_TUDataset_from_gxl;
import org.jgrapht.UndirectedGraph;
import org.jgrapht.graph.SimpleGraph;
import graph_element.*;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Stack;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.Callable;
import java.util.concurrent.CyclicBarrier;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Random;

/**
 * Created by user on 27/03/2017.
 */
public class Main {

    private static int cost_node_sub = 0;
    private static int cost_node_del_ins = 0;

    private static int cost_edge_sub = 0;
    private static int cost_edge_del_ins = 0;

    public static Parallel fin = new Parallel();
    public static String file_g1 = null;
    public static String file_g2 = null;

    private static PrintWriter out = null;

    private static String separator = ";";
    public static int NB_thread = 10;

    public static UndirectedGraph<Vertex, Edge> g1 = null;
    public static UndirectedGraph<Vertex, Edge> g2 = null;
    public static UndirectedGraph<Vertex, Edge> g3 = null;
    //public static int UB =10000;
    public static Stack<Path> path_Stack_load;
    public static Queue<Path> path_Stack;

    public static String Final_results = "";
    public static AtomicInteger upper_bound = new AtomicInteger(1000);
    public static int global_visited_nodes = 0;
    public static CyclicBarrier barrier;
    //public static int k_level = 500;
    public static int k_level = 1000;

    public static int amount_RunTime_S = 0;

    static Comparator<Path> idComparator = new Comparator<Path>() {
        @Override
        public int compare(Path c1, Path c2) {
            return (int) (-c1.getG_cost() + c2.getG_cost());
            //return (int) (c1.getRemaining_unprocessed_vertex_g2().size() - c2.getRemaining_unprocessed_vertex_g2().size());
            //  return (int) (c1.getG_cost_PLUS_h_cost() - c2.getG_cost_PLUS_h_cost());
            //    return (int) (1*(c1.getIndex_processed_vertices_g1() - c2.getIndex_processed_vertices_g1()));
        }
    };

    public static void main(String[] args) {
        path_Stack_load = new Stack<Path>();
        path_Stack = new PriorityQueue<>(idComparator);
        // P_path_Stack.
        String pathname_result_output_file = null;
        String test_benchmark = null; // CMU, MUTA, GREC, PATH (acyclic, alkane, pah, mao)

        upper_bound.set(1000);
        if (args.length >= 10) {
            try {
                cost_node_sub = Integer.parseInt(args[0]);
                cost_node_del_ins = Integer.parseInt(args[1]);
                cost_edge_sub = Integer.parseInt(args[2]);
                cost_edge_del_ins = Integer.parseInt(args[3]);

                file_g1 = args[4];
                file_g2 = args[5];

                pathname_result_output_file = args[6];

                test_benchmark = args[7];

                amount_RunTime_S = Integer.parseInt(args[8]);

                NB_thread = Integer.parseInt(args[9]);

            } catch (NumberFormatException e) {
                System.err.println("Argument : " + e.getMessage() + " must be an integer.");
                System.exit(1);
            }
        }


        if (test_benchmark.equals("PATH")) {
            Main.g1 = Import_JGraphT_From_GXL.import_simple_graph(file_g1);
            g2 = Import_JGraphT_From_GXL.import_simple_graph(file_g2);
        } else if (test_benchmark.equals("GREC")) {
            g1 = Import_JGraphT_From_GXL.import_simple_graph_from_GREC_GED(file_g1);
            g2 = Import_JGraphT_From_GXL.import_simple_graph_from_GREC_GED(file_g2);
        } else if (test_benchmark.equals("MUTA")) {
            g1 = Import_JGraphT_From_GXL.import_simple_graph_from_MUTA_GED(file_g1);
            g2 = Import_JGraphT_From_GXL.import_simple_graph_from_MUTA_GED(file_g2);
        } else if (test_benchmark.equals("CMU")) {
            g1 = Import_JGraphT_From_GXL.import_simple_graph_from_CMU_GED(file_g1);
            g2 = Import_JGraphT_From_GXL.import_simple_graph_from_CMU_GED(file_g2);
        }else if (test_benchmark.equals("TUDataset")) {
            g1 = Import_TUDataset_from_gxl.import_simple_graph_label_only(file_g1);
            g2 = Import_TUDataset_from_gxl.import_simple_graph_label_only(file_g2);
        }


        if (g1 == null) {
            System.out.println("Can't Load the First Graph : " + file_g1);
            return;
        }
        if (g2 == null) {
            System.out.println("Can't Load the Second Graph : " + file_g2);
            return;
        }

        if (g1.vertexSet().size() > g2.vertexSet().size()) {
            g3 = g1;
            g1 = g2;
            g2 = g3;
            System.out.println("Switching graphs g1 and g2 ");
        }

        barrier = new CyclicBarrier(NB_thread);
        //Exact_GED_AStar exact_GED = new Exact_GED_AStar();
        Exact_GED_BB_DF exact_GED = new Exact_GED_BB_DF(amount_RunTime_S);

        GED_Operations_Cost.setAll_Operations_cost(cost_node_sub, cost_node_del_ins, cost_node_del_ins, cost_edge_sub, cost_edge_del_ins, cost_edge_del_ins, 1);

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
        long startTime = System.nanoTime();

        double editDistance = 0;//exact_GED.computeGED(g1,g2);

        long endTime = System.nanoTime();

        long elapsedTime = endTime - startTime;

        for (int i = 1; i < NB_thread + 1; i++) {
            Parallel T1 = new Parallel();
            T1.Parallel("thread-" + i);
            T1.start();
        }
        // ---------------------------------------------------------------------------------------
        // ---------------------------------------------------------------------------------------

        /// String output= "test__"+new File(file_g1).getName()+"__"+new File(file_g2).getName();
        synchronized (fin) {
            try {
                //  System.out.println("Waiting for threads to finish...NB_threads"+NB_thread);
                //  for(int i=0;i<NB_thread;i++){
                fin.wait(); //System.out.println("i:"+i);}
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            // System.out.println("the end of threads execution");
        }

        try {
            File file = new File(pathname_result_output_file);

            if (file.getParentFile() != null) {
                file.getParentFile().mkdirs();
            }

            out = new PrintWriter(new FileWriter(file, true), true);
            out.println("Final_results:" + Final_results);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (out != null)
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
