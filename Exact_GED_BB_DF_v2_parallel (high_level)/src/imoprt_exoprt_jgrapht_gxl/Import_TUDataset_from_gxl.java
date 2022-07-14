/**
 * Created by ibra on 24/05/2022.
 */

package imoprt_exoprt_jgrapht_gxl;

import graph_element.Edge;
import graph_element.Vertex;
import net.sourceforge.gxl.*;
import org.jgrapht.UndirectedGraph;
import org.jgrapht.graph.SimpleGraph;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class Import_TUDataset_from_gxl {

    // TUDataset :
    // Vertex label (int), attributes (a vector of float)
    // Edge   label (int), attributes (a vector of float)
    // label is in the first attr as : "<attr name=\"label\"><int>{}</int> </attr>"
    // attributes are from the second attr as : "<attr name=\"attr\"><float>{}</float> </attr>"
    // vertex Id begin from 1.
    // vertex id : "<node id=\"{}\">"

    public static UndirectedGraph<Vertex, Edge> import_simple_graph_label_only(String gxl_path_file)
    {
        UndirectedGraph<Vertex, Edge> graph_JGJ = new SimpleGraph(Edge.class);

        try {
            File gxlFile = new File(gxl_path_file);
            GXLDocument gxlDocument = new GXLDocument(gxlFile);


            GXLGraph graph_GXL = gxlDocument.getDocumentElement().getGraphAt(0);

            GXLNode gxlNode;
            GXLEdge gxlEdge;
            GXLAttr gxlAttr;
            GXLInt gxlInt;

            int nodeId;
            int nodeValue;

            int edgeValue;

            int nb_element = graph_GXL.getGraphElementCount();

            int nbNode = nb_element; // we supose that all element are node, because here we can't risk, unless we find a fast methode to know the number of nodes

            // create a map of vertex id to vertex
            // key : vertex id
            // value : vertex
            // we will use this map to check from and to vertex exits before creating the edge.
            Map<Integer, Vertex> map_vertex_id_to_vertex = new HashMap<>();

            for (int i = 0; i < nb_element; i++)
            {
                GXLElement graphElement = graph_GXL.getGraphElementAt(i);

                // print the element and its type
                // System.out.println("Element : " + graphElement.toString() + " type : " + graphElement.getClass().getName());

                if (graphElement instanceof GXLNode)
                {
                    gxlNode = ((GXLNode) graphElement);
                    nodeId = Integer.parseInt((gxlNode.getID()));

                    gxlAttr = gxlNode.getAttrAt(0); // label is in the first attribute

                    gxlInt = (GXLInt) gxlAttr.getChildAt(0);

                    nodeValue = gxlInt.getIntValue();

                    Vertex v = new Vertex(nodeId, nodeValue);

                    graph_JGJ.addVertex(v);

                    // add the vertex to the map
                    map_vertex_id_to_vertex.put(nodeId, v);

                } else if (graphElement instanceof GXLEdge) {
                    gxlEdge = (GXLEdge) graphElement;

                /*System.out.println(" Edge : "+((GXLEdge) graphElement).getID()+
                        "| form: "+((GXLEdge) graphElement).getSourceID()+
                        "--> to : "+((GXLEdge) graphElement).getTargetID());*/

                    int nodeID_from = Integer.parseInt(((GXLEdge) graphElement).getSourceID());
                    int nodeID_to = Integer.parseInt(((GXLEdge) graphElement).getTargetID());

                    edgeValue = ((GXLInt) (gxlEdge.getAttrAt(0).getChildAt(0))).getIntValue();

                    // check if the from and to vertex exits
                    if (map_vertex_id_to_vertex.containsKey(nodeID_from) && map_vertex_id_to_vertex.containsKey(nodeID_to))
                    {
                        Vertex v_from = map_vertex_id_to_vertex.get(nodeID_from);
                        Vertex v_to = map_vertex_id_to_vertex.get(nodeID_to);

                        Edge myEdge = graph_JGJ.addEdge(v_from, v_to);

                        // if myEdge is null, it means that the edge already exists
                        // which mean that we anothor edge with the same from and to vertex
                        // and this is not allowed in simple graph
                        // in this case we take only the first edge found, and ignor all others

                        if (myEdge != null)
                        {
                            myEdge.setWeight(edgeValue); // because label is int and not string
                        }
                        else{
                            System.out.println("Edge already exists : " + nodeID_from + " --> " + nodeID_to);
                        }
                    }
                }
            }

        }catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (SAXException e) {
            e.printStackTrace();
        }

        return graph_JGJ;
    }

}
