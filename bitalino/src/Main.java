//package src;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;

public class Main {

    public static Frame[] frame;
    public static int[] params;
    private static String paramString;

    private static ServerSocketChannel serverSocket=null;    

    private static void setUpSocket(){

        try {
            serverSocket = ServerSocketChannel.open();
            InetSocketAddress serverIPAddr = new InetSocketAddress("127.0.0.1",50500);
            serverSocket.bind(serverIPAddr);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

    
    public static void main(String[] args) {

        if(args.length != 2){
            System.exit(-1);
        }

        String macAddress = args[0];
        int iterations = Integer.parseInt(args[1]);

        SocketChannel s=null;
        try {
            setUpSocket();
            s = serverSocket.accept();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            System.exit(-1);
        }

        BITalino bitalino = new BITalino();

    
        try{
            macAddress = "20:17:11:20:51:54"; //TODO remove this
            iterations = 10;
            
            int SamplingRate = 10;
            bitalino.open(macAddress, SamplingRate);
        
            int[] channelsToAcquire = {1,};
            bitalino.start(channelsToAcquire);
        

            int block_size=10;
                // Param1[block_size*sample_iterations] == [param(0), param(1), param(2), ..., param(99999999)]
                // Param2[block_size*sample_iterations]
            params = new int[block_size*iterations];


            for (int j = 0; j < iterations; j++) {
        
                //Each time read a block of 10 samples 
                frame = bitalino.read(block_size);
                

                for (int i = 0; i < frame.length; i++) {
                    params[i+j*block_size]=frame[i].analog[0];

                    if(i==0){
                        paramString=""+frame[i].analog[0]+" ";
                    }else{
                        paramString+=frame[i].analog[0]+" ";
                    }
                        
                }

                s.write(ByteBuffer.wrap(paramString.getBytes("utf8")));

            }
            //stop acquisition
            bitalino.stop();
        } catch (BITalinoException ex) {
            System.out.print("FUck1");
        } catch (Throwable ex) {
            System.out.print("FUck2");
        } finally {
            try {
                //close bluetooth connection
                if (bitalino != null) {
                    bitalino.close();
                }
                s.close();
                serverSocket.close();
            } catch (BITalinoException ex) {
                System.out.print("FUck3");
            } catch(IOException ex2){
                System.out.println("Fuck off");
            }
        }
    }


}
