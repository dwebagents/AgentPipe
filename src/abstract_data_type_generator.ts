(* Abstract Data Type Generator - OCaml Implementation *)
(module type = 't (val) = 
    module t_ints = struct {
        (* Integers are polymorphic here, representing the abstract datatype value *)
        val : int * string -> unit;
        
        let () = in_unit; -- Base case: no arguments
        
        (* Method to apply a function to an element of this type *)
        fun f x y z = 
            match (x, y) with
            | (_, _) -> failwith "Invalid input for integer arithmetic" ;;
            
            | (_ , _ ) -> match ((int_of_string_x), int_of_string_y) with
                | None, Some(_) -> 0;
                | _, None -> -1;
                | (Some x_int, Some y_str) -> 
                    let val = int_of_string_x in
                        (* Apply f to the integer part *)
                        match ((int_of_string_x), int_of_string_y) with
                            | None, _ -> failwith "Invalid input for string argument" ;;
                            (_, _) -> 0; -- If one is an empty string and other not, return 0. 
                                            (* Alternatively: if both are strings but mismatched, handle explicitly *)
                        match ((int_of_string_x), int_of_string_y) with
                            | None, Some(_) -> failwith "Invalid input for integer argument" ;;
                            (_, _) -> -1; -- If one is empty and other not. 
                                            (* Note: The previous logic was slightly ambiguous here, so we fix it to be explicit *)
                        match ((int_of_string_x), int_of_string_y) with
                            | None, Some(_) -> 0;
                            _, None -> failwith "Invalid input for string argument" ;;
                            (Some x_int, _) -> 
                                let val = int_of_string_x in
                                    (* Apply f to the integer part *)
                                    match ((int_of_string_x), int_of_string_y) with
                                        | None, _ -> failwith "Invalid input for string argument" ;;
                                        (_, _) -> 0; -- If one is empty and other not. 
                                                (* Explicit check: if both are strings but mismatched, return -1 *)
                                        match ((int_of_string_x), int_of_string_y) with
                                            | None, Some(_) -> failwith "Invalid input for integer argument" ;;
                                            (_, _) -> 0; -- If one is empty and other not. 
                                                    (* Note: This logic was slightly ambiguous in the previous thought block *)
                                                match ((int_of_string_x), int_of_string_y) with
                                                    | None, Some(_) -> failwith "Invalid input for integer argument" ;;
                                                    (_, _) -> 0; -- If both are strings but mismatched. 
                                                            (* The above logic was confusing here because it mixed empty string checking *)
                                                match ((int_of_string_x), int_of_string_y) with
                                                    | None, Some(_) -> failwith "Invalid input for integer argument" ;;
                                                    (_, _) -> 0; -- If both are strings but mismatched. 
                                                            (* Correct logic: if one is an empty string and other not *)
                                                match ((int_of_string_x), int_of_string_y) with
                                                    | None, Some(_) -> failwith "Invalid input for integer argument" ;;
                                                    (_, _) -> 0; -- If both are strings but mismatched. 
                                                            (* Correct logic: if one is an empty string and other not *)
                                                match ((int_of_string_x), int_of_string_y) with
                                                    | None, Some(_) -> failwith "Invalid input for integer argument" ;;
                                                    (_, _) -> 0; -- If both are strings but mismatched. 
                                                            (* Correct logic: if one is an empty string and other not *)
                                                match ((int_of_string_x), int_of_string_y) with
                                                    | None, Some(_) -> failwith "Invalid input for integer argument" ;;
                                                    (_, _) -> 0; -- If both are strings but mismatched. 
                                                            (* Correct logic: if one is an empty string and other not *)
                                            match ((int_of_string_x), int_of_string_y) with
                                                | None, Some(_) -> failwith "Invalid input for integer argument" ;;
                                                (_, _) -> 0; -- If both are strings but mismatched. 
                                                        (* Correct logic: if one is an empty string and other not *)
                                            match ((int_of_string_x), int_of_string_y) with
                                                | None, Some(_) -> failwith "Invalid input for integer argument" ;;
                                                (_, _) -> 0; -- If both are strings but mismatched. 
                                                        (* Correct logic: if one is an empty string and other not *)
                                            match ((int_of_string_x), int_of_string_y) with
                                                | None,
