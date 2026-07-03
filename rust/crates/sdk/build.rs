use std::path::PathBuf;

fn main() {
    let proto_dir = PathBuf::from("../../proto");
    let proto_root = proto_dir.join("cowabunga_sdk");
    let out_dir = PathBuf::from("src/generated");

    std::fs::create_dir_all(&out_dir).expect("failed to create generated output directory");

    let protos: Vec<PathBuf> = walkdir::WalkDir::new(&proto_root)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| {
            e.file_type().is_file()
                && e.path().extension().and_then(|s| s.to_str()) == Some("proto")
        })
        .map(|e| e.path().to_path_buf())
        .collect();

    if protos.is_empty() {
        panic!("No .proto files found under {:?}", proto_root);
    }

    tonic_build::configure()
        .out_dir(&out_dir)
        .include_file("mod.rs")
        .compile_protos(&protos, &[proto_dir])
        .expect("Failed to compile protobufs");

    for proto in &protos {
        println!("cargo:rerun-if-changed={}", proto.display());
    }
}
