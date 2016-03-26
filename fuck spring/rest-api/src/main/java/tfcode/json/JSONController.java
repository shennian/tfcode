package tfcode.json;


import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import com.google.gson.JsonParser;

import tfcode.template.TFTemplate;


@Controller
@RequestMapping("/hello")
public class JSONController{
	ApplicationContext context = 
    		new ClassPathXmlApplicationContext("spring-datasource.xml");
	TFTemplate fuck = (TFTemplate) context.getBean("TFTemplate");
	
    @RequestMapping(method = RequestMethod.GET)
    public @ResponseBody String toJson() {
    	System.out.println("fuck");
    	String sql = "select link_id count where kw=logo…Ëº∆";
    	return new JsonParser().parse(fuck.test()).toString();
   }

}