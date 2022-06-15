import java.util.ArrayList;
import java.util.List;

public class test {
    public static void main(String[] args) {
        int nowPage = 11;
        int subPage = (nowPage - 1) / 10;
        int lastPage = 13;

        List<Integer> list2 = new ArrayList<>();

        // subPage 이용하는 방법 => 10단위씩 보여주게 된다.(1~10 , 11~20)
        for (int i = (0 + (10 * subPage)); i < 10 * (1 + subPage); i++) {
            if (i + 1 > lastPage) {
                break;
            }
            list2.add(i + 1);
        }
        System.out.println(list2);
    }
}