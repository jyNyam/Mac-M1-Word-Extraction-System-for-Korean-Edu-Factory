
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // [중요] 매니저님의 Supabase 정보로 꼭 수정하세요!
  await Supabase.initialize(
    url: 'https://kggpojguiwnzmikibhzn.supabase.co',
    anonKey: 'sb_publishable_rFVuNo9uGALWqk5cUIEoAw_lXR2S2jH',
  );
  runApp(const CoreWorkApp());
}

class CoreWorkApp extends StatelessWidget {
  const CoreWorkApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CoreWork Word Factory',
      debugShowCheckedModeBanner: false, // 오른쪽 상단 DEBUG 띠 제거
      theme: ThemeData(primarySwatch: Colors.indigo, useMaterial3: true),
      home: const DashboardPage(),
    );
  }
}

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  final supabase = Supabase.instance.client;

  // 'auto_labeled' 상태인 단어만 실시간으로 가져오는 통로
  final Stream<List<Map<String, dynamic>>> _stream = Supabase.instance.client
      .from('industry_keywords')
      .stream(primaryKey: ['id'])
      .order('id', ascending: false);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🏭 단어 분류 공장 (Reviewer)'),
        backgroundColor: Colors.indigo.shade50,
      ),
      body: StreamBuilder<List<Map<String, dynamic>>>(
        stream: _stream,
        builder: (context, snapshot) {
          if (snapshot.hasError) return Center(child: Text("에러 발생: ${snapshot.error}"));
          if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
          
          // AI가 추천한(auto_labeled) 데이터만 필터링
          final items = snapshot.data!.where((row) => row['status'] == 'auto_labeled').toList();

          if (items.isEmpty) {
            return const Center(child: Text("✨ 검토할 단어가 없습니다! 모든 작업이 완료되었습니다."));
          }

          return ListView.builder(
            itemCount: items.length,
            itemBuilder: (context, index) {
              final item = items[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                elevation: 2,
                child: ListTile(
                  title: Text(item['term'], style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Colors.indigo)),
                  subtitle: Text("🤖 AI 추천: ${item['sub_category']}\n📄 출처: ${item['source_ref']}"),
                  trailing: ElevatedButton.icon(
                    onPressed: () => _confirmCategory(item['id'], item['sub_category']),
                    icon: const Icon(Icons.check),
                    label: const Text("확정"),
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.indigo.shade50),
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }

  // 확정 버튼 로직: 상태를 active로 바꾸고 괄호를 제거함
  Future<void> _confirmCategory(int id, String suggested) async {
    final confirmedSub = suggested.replaceAll(RegExp(r'검토필요\(|\)'), '');
    await supabase.from('industry_keywords').update({
      'sub_category': confirmedSub,
      'status': 'active',
      'updated_at': DateTime.now().toIso8601String(),
    }).eq('id', id);
    
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('✅ [${confirmedSub}] 카테고리로 확정되었습니다!'), duration: const Duration(seconds: 1)),
      );
    }
  }
}