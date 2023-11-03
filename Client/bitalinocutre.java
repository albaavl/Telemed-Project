import bitalino.*;

public class bitalinocutre {

    public static Frame[] frame;
    public static int[] params;

    
    public static void dothethingy(String macAddress, int iterations){
    
        BITalino bitalino = new BITalino();

    
        try{
            macAddress = "20:17:11:20:51:54";
            
            int SamplingRate = 10;
            bitalino.open(macAddress, SamplingRate);
        
            int[] channelsToAcquire = {1,};
            bitalino.start(channelsToAcquire);
        
            //Read in total 10000000 times 10million times == 100million samples total
            //100 000 000 ==  21 chars per sample should be enough, change TEXT for LONGTEXT == 2x(2.147.483.647 == max string size for java) 
            //  iterations=10000000;
            int block_size=10;
                // Param1[block_size*sample_iterations] == [param(0), param(1), param(2), ..., param(99999999)]
                // Param2[block_size*sample_iterations]
            params = new int[block_size*iterations];


            for (int j = 0; j < iterations; j++) {
        
                //Each time read a block of 10 samples 
                frame = bitalino.read(block_size);
                

                    for (int i = 0; i < frame.length; i++) {
                        params[i+j*block_size]=frame[i].analog[0];
                        // params[1][i]=frame[i].analog[1];
                    // params[i][] = ;
                }

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
            } catch (BITalinoException ex) {
                System.out.print("FUck3");
            }
        }

        
        }

}
