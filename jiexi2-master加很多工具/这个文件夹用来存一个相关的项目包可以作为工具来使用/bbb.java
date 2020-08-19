//这个java文件的说明,这个文件是java来调用这个nlp项目的接口调用方法.注意一点是form-data格式就好了.


package 接口测试;

import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.AsyncRestOperations;
import org.springframework.web.client.RestTemplate;

public class bbb {


    public static void main(String[] args) throws JSONException {


        RestTemplate restTemplate = new RestTemplate();
        MultiValueMap<String, String> map = new LinkedMultiValueMap<String, String>();

        map.add("url","https://nanjing.s3.cn-north-1.jdcloud-oss.com/nanjing/132.rar");
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<MultiValueMap<String, String>>(
                map, headers);

        ResponseEntity<String> responseEntity = restTemplate.postForEntity("http://116.196.87.166:8082/master", request, String.class);

//
//        HttpHeaders headers = new HttpHeaders();
//        MediaType type = MediaType.parseMediaType("application/json; charset=UTF-8");
//        headers.setContentType(type);
//        headers.add("Accept", MediaType.APPLICATION_JSON.toString());
//        HttpEntity<String> formEntity = new HttpEntity<String>(json.toString(), headers);
//        RestTemplate restTemplate = new RestTemplate();
//        String s= restTemplate.postForEntity("http://116.196.87.166:8082/master",formEntity,String.class).getBody();
    }
}
