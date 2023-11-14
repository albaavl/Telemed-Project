package src;

/// A frame returned by BITalino.read()
public class Frame {
        /// CRC4 check function result for the frame
	public int CRC;

        /// %Frame sequence number (0...15).
        /// This number is incremented by 1 on each consecutive frame, and it overflows to 0 after 15 (it is a 4-bit number).
        /// This number can be used to detect if frames were dropped while transmitting data.
	public int seq;

        /// Array of analog inputs values (0...1023 on the first 4 channels and 0...63 on the remaining channels)
	public int [] analog = new int[6];

        /// Array of digital ports states (false for low level or true for high level).
        /// On original %BITalino, the array contents are: I1 I2 I3 I4.
        /// On %BITalino (r)evolution, the array contents are: I1 I2 O1 O2.
	public int [] digital = new int[4];

}
