
/**
 * Created by user on 26/04/2017.
 */

import graph_element.Edge;
import graph_element.Vertex;

public class GED_Operations_Cost {

    private static int vertex_substitution_cost = 1;
    private static int vertex_insertion_cost = 1;
    private static int vertex_deletion_cost = 1;

    private static int edge_substitution_cost = 1;
    private static int edge_insertion_cost = 1;
    private static int edge_deletion_cost = 1;

    private static int unit_cost = 1;

    private static boolean is_Weight=false; // if the graph use weight (true) or not (false)
    private static boolean is_Label=false; // if the graph use label string (true)  or not (false)

    private GED_Operations_Cost() {
    }

    public static int getVertex_substitution_cost() { return vertex_substitution_cost; }

    public static int getVertex_insertion_cost() { return vertex_insertion_cost; }

    public static int getVertex_deletion_cost() { return vertex_deletion_cost; }

    public static int getEdge_substitution_cost() { return edge_substitution_cost; }

    public static int getEdge_insertion_cost() { return edge_insertion_cost; }

    public static int getEdge_deletion_cost() { return edge_deletion_cost; }

    public static boolean isIs_Weight() {
        return is_Weight;
    }

    public static boolean isIs_Label() {
        return is_Label;
    }

    public static int getUnit_cost() { return unit_cost; }

    public static void setVertex_substitution_cost(int vertex_substitution_cost) {
        GED_Operations_Cost.vertex_substitution_cost = vertex_substitution_cost;
    }

    public static void setVertex_insertion_cost(int vertex_insertion_cost) {
        GED_Operations_Cost.vertex_insertion_cost = vertex_insertion_cost;
    }

    public static void setVertex_deletion_cost(int vertex_deletion_cost) {
        GED_Operations_Cost.vertex_deletion_cost = vertex_deletion_cost;
    }

    public static void setEdge_substitution_cost(int edge_substitution_cost) {
        GED_Operations_Cost.edge_substitution_cost = edge_substitution_cost;
    }

    public static void setEdge_insertion_cost(int edge_insertion_cost) {
        GED_Operations_Cost.edge_insertion_cost = edge_insertion_cost;
    }

    public static void setEdge_deletion_cost(int edge_deletion_cost) {
        GED_Operations_Cost.edge_deletion_cost = edge_deletion_cost;
    }

    public static void setUnit_cost(int unit_cost) {
        GED_Operations_Cost.unit_cost = unit_cost;
    }

    public static void setIs_Weight(boolean is_Weight) {
        GED_Operations_Cost.is_Weight = is_Weight;
    }

    public static void setIs_Label(boolean is_Label) {
        GED_Operations_Cost.is_Label = is_Label;
    }

    public static void setAll_Operations_cost(int vertex_substitution_cost,
                                              int vertex_insertion_cost,
                                              int vertex_deletion_cost,
                                              int edge_substitution_cost,
                                              int edge_insertion_cost,
                                              int edge_deletion_cost,
                                              int unit_cost)
    {

        GED_Operations_Cost.vertex_substitution_cost = vertex_substitution_cost;
        GED_Operations_Cost.vertex_insertion_cost = vertex_insertion_cost;
        GED_Operations_Cost.vertex_deletion_cost = vertex_deletion_cost;
        GED_Operations_Cost.edge_substitution_cost = edge_substitution_cost;
        GED_Operations_Cost.edge_insertion_cost = edge_insertion_cost;
        GED_Operations_Cost.edge_deletion_cost = edge_deletion_cost;
        GED_Operations_Cost.unit_cost = unit_cost;
    }

    public static int getOperationCost(GED_Operations operation_type)
    {
        switch (operation_type)
        {
            case Vertex_DELETION: return vertex_deletion_cost;
            case Vertex_INSERTION: return vertex_insertion_cost;
            case Vertex_SUBSTITUTION: return vertex_substitution_cost;

            case Edge_DELETION: return edge_deletion_cost;
            case Edge_INSERTION: return edge_insertion_cost;
            case Edge_SUBSTITUTION: return edge_substitution_cost;

            default: return unit_cost;
        }
    }


    public static int getVertex_substitution_cost(Vertex fromVertex, Vertex toVertex)
    {
        if(is_Weight)
        {
            if(fromVertex.getVertex_weight()==toVertex.getVertex_weight()) return 0;
        }

        if(is_Label)
        {
            if(fromVertex.getVertexLabel().equals(toVertex.getVertexLabel())) return 0;

            // give the cost of the substitution based on the Vertex Label Edit Distance (string distance)
            /// return (SED(v1.getVertexLabel(),v2.getVertexLabel()));
        }

        // else, return the substitution cost.
        return vertex_substitution_cost;
    }

    public static int getEdge_substitution_cost(Edge e1, Edge e2)
    {

        if(is_Weight) {
            if(e1.getWeight()==e2.getWeight()) return 0;
        }

        if(is_Label)
        {
            if(e1.getEdgeLabale()==null && e2.getEdgeLabale()==null) return 0;

            if(e1.getEdgeLabale()!=null && e2.getEdgeLabale()!=null){
                if(e1.getEdgeLabale().equals(e2.getEdgeLabale())) return 0;
            }

            /// return SED(e1.getEdgeLabel(),e2.getEdgeLabel());
        }


        return edge_substitution_cost;
    }
}
