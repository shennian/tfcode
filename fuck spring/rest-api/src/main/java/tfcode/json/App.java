package tfcode.json;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import tfcode.template.TFTemplate;

public class App {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		ApplicationContext context = 
	    		new ClassPathXmlApplicationContext("spring-datasource.xml");
		TFTemplate fuck = (TFTemplate) context.getBean("TFTemplate");
		fuck.test();

	}

}
