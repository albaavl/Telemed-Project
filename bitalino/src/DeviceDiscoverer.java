//package src;

import java.util.Vector;
import javax.bluetooth.DeviceClass;
import javax.bluetooth.DiscoveryAgent;
import javax.bluetooth.DiscoveryListener;
import javax.bluetooth.LocalDevice;
import javax.bluetooth.RemoteDevice;
import javax.bluetooth.ServiceRecord;

public class DeviceDiscoverer implements DiscoveryListener {


    public Vector<RemoteDevice> remoteDevices = new Vector<RemoteDevice>();
    DiscoveryAgent discoveryAgent;
    public String deviceName;
    String inqStatus = null;

    public DeviceDiscoverer() {
        try {
            LocalDevice localDevice = LocalDevice.getLocalDevice();
            System.err.println(LocalDevice.getLocalDevice());
            discoveryAgent = localDevice.getDiscoveryAgent();
            discoveryAgent.startInquiry(DiscoveryAgent.GIAC, this);            

        } catch(Exception e) {
            e.printStackTrace();
        }
    }

    public void deviceDiscovered(RemoteDevice remoteDevice, DeviceClass cod) {
        
    	try
    	{
           deviceName=remoteDevice.getFriendlyName(false); //Records devices names
           if (deviceName.equalsIgnoreCase("bitalino")) 
           {
	           remoteDevices.addElement(remoteDevice);
           }
          
        } 
    	catch(Exception e)
        {
            e.printStackTrace();
        }
    }

    public void inquiryCompleted(int discType) 
    {
    
	    if (discType == DiscoveryListener.INQUIRY_COMPLETED) 
	    {
	        inqStatus = "Scan completed.";
	    }
	    else if (discType == DiscoveryListener.INQUIRY_TERMINATED) 
	    {
	        inqStatus = "Scan terminated.";
	    }
	    else if (discType == DiscoveryListener.INQUIRY_ERROR) 
	    {
	        inqStatus = "Scan with errors.";
	    }
    }

    public void servicesDiscovered(int transID, ServiceRecord[] servRecord){}

    public void serviceSearchCompleted(int transID, int respCode) {}
}
