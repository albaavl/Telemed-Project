package bitalino;

public class BITalinoException extends java.lang.Exception {
	
	private static final long serialVersionUID = 1L;

	public BITalinoException(BITalinoErrorTypes errorType) {
		super(errorType.getName());
	    code = errorType.getValue();
	}
	
	public int code;

}
