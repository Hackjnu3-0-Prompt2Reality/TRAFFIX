import java.util.*;

public class Main {
    public static void FrontToLast(Queue<Integer> q, int qsize)
    {
        if (qsize <= 0)
            return;
        q.add(q.peek());
        q.remove();
        FrontToLast(q, qsize - 1);
    }

    public static void pushInQueue(Queue<Integer> q,
                                   int temp, int qsize)
    {
        if (q.isEmpty() || qsize == 0)
        {
            q.add(temp);
            return;
        }
        else if (temp <= q.peek())
        {
            q.add(temp);
            FrontToLast(q, qsize);
        }
        else
        {
            q.add(q.peek());
            q.remove();
            pushInQueue(q, temp, qsize - 1);
        }
    }
    public static void sortQueue(Queue<Integer> q)
    {
        if (q.isEmpty())
            return;
        int temp = q.peek();
        q.remove();
        sortQueue(q);
        pushInQueue(q, temp, q.size());
    }
    public static void sortDesc(Queue<Integer> q){
        Stack s = new Stack<>();
        while(!q.isEmpty()){
            s.add(q.poll());
        }
        while(!s.isEmpty()){
            q.add((Integer) s.pop());
        }
    }
    public static Queue<Integer> getOperation(int[] cluster){
        Queue<Integer> ql0 = new LinkedList<>(); //works on lane
        Queue<Integer> ql1 = new LinkedList<>(); //works on lane
        Queue<Integer> ql2 = new LinkedList<>(); //works on lane
        Queue<Integer> ql3 = new LinkedList<>(); //works on lane
        Queue<Integer> maxHeap = new LinkedList<>(); //works on cluster level
        int lanes = 4;
        if(cluster[0] == 0 && cluster[1] == 0 && cluster[2] == 0 && cluster[3] == 0){
            System.out.println("Default algo");
        }
        for(int i = 0; i < lanes; i++) {
            if (cluster[i] == 1) {
                ql1.add(i + 1);
            } else if (cluster[i] == 2) {
                ql2.add(i + 1);
            } else if (cluster[i] == 3) {
                ql3.add(i + 1);
            } else if (cluster[i] == 0) {
                ql0.add(i + 1);
            }
        }
        for(int i: cluster){
            maxHeap.add(i);
        }
//        System.out.println("zero queue" + ql0);
//        System.out.println("one queue" + ql1);
//        System.out.println("two queue" + ql2);
//        System.out.println("three queue" + ql3);
//        System.out.println("maxStack" + maxHeap);
        int maxLen = Math.max(ql0.size(), Math.max(ql1.size(), Math.max(ql2.size(), Math.max(ql3.size(), maxHeap.size()))));
        Queue<Integer> operationToPerform;
        if(maxLen == ql0.size()){
            operationToPerform = ql0;
        } else if (maxLen == ql1.size()) {
            operationToPerform = ql1;
        } else if (maxLen == ql2.size()) {
            operationToPerform = ql2;
        } else if (maxLen == ql3.size()) {
            operationToPerform = ql3;
        }
        else {
            sortQueue(maxHeap);
            sortDesc(maxHeap);
            operationToPerform = maxHeap;
        }
        return operationToPerform;
    }
    public static void main(String[] args) {
        int cluster[] = new int[4];
        HashMap<Integer, Integer> map = new HashMap<>();
        Scanner sc = new Scanner(System.in);
        for(int i = 1; i <= cluster.length; i++){
            int n = sc.nextInt();
            cluster[i - 1] = n;
            map.put(n, i);
        }

        int[] time = new int[4];
        int tmp = 0;
        int tMax = 64;
        Queue<Integer> fnl = getOperation(cluster);
        while(!fnl.isEmpty()){
            int curntLevel = fnl.poll();
            if(curntLevel == 1){
                int t = tMax / 8 ;
                if(curntLevel == 2){
                    tmp = tMax / (4 * 2) ;
                } else if (curntLevel == 3) {
                    tmp = tMax / (2 * 2);
                }
                t = t + tmp;
                time[map.get(curntLevel) - 1] = t;
            }
            else if(curntLevel == 2) {
                int t = tMax / 4;
                if (curntLevel == 3) {
                    tmp = tMax / (2 * 2);
                }
                t = t + tmp;
                time[map.get(curntLevel) - 1] = t;
            }
            else if(curntLevel == 3){
                int t = tMax / 2;
                time[map.get(curntLevel) - 1] = t;
            }
        }
        System.out.println(fnl);
        System.out.println(map);
        for(int i: time){
            System.out.print(i + " ");
        }
        System.out.println();
    }
}